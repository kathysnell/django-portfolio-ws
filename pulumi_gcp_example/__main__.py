import pulumi
import pulumi_gcp as gcp
import pulumi_random as random

### --- Initialize Pulumi configuration ---
config = pulumi.Config()
project = config.require("project")
region = config.get("region") or "us-central1"

### --- Create service account if needed ---
sa = gcp.serviceaccount.Account("pws-cloud-run-sa", account_id="pws-cloud-run-sa-v1")

### --- SECRET MANAGEMENT ---
### --- Define your secrets and their desired lengths
secrets_config = {
    "pws-db-password": 32,
}

pws_secret_versions = {}

for secret_id, length in secrets_config.items():
    
    ### --- Generate a random value
    rnd_password = random.RandomPassword(f"rnd-{secret_id}",
        length=length,
        special=True)

    ### --- Create the Secret container
    secret_container = gcp.secretmanager.Secret(f"sec-{secret_id}",
        secret_id=secret_id,
        replication={"auto": {},})

    ### --- Create the Secret Version using the random value
    secret_version = gcp.secretmanager.SecretVersion(f"ver-{secret_id}",
        secret=secret_container.id,
        secret_data=rnd_password.result)
    
    ### --- Save for access
    pws_secret_versions[secret_id] = secret_version

    ### --- Grant the Service Account access to THIS specific secret
    gcp.secretmanager.SecretIamMember(f"iam-{secret_id}",
        secret_id=secret_container.id,
        role="roles/secretmanager.secretAccessor",
        member=sa.email.apply(lambda email: f"serviceAccount:{email}"))

### --- NETWORKING AND VPC MANAGEMENT ---
vpc = gcp.compute.Network("pws-network", auto_create_subnetworks=False)

pws_cloud_run_subnet = gcp.compute.Subnetwork("pws-cloud-run-subnet",
    network=vpc.id,
    ip_cidr_range="10.0.2.0/24",
    region=region,
    private_ip_google_access=True) # Required for VPC -> GCS/IAM traffic

pws_private_ip_alloc = gcp.compute.GlobalAddress("pws-private-ip-alloc",
    purpose="VPC_PEERING",
    address_type="INTERNAL",
    prefix_length=24,
    network=vpc.id)

pws_private_vpc_connection = gcp.servicenetworking.Connection("pws-private-vpc-connection",
    network=vpc.id,
    service="servicenetworking.googleapis.com",
    reserved_peering_ranges=[pws_private_ip_alloc.name])

pws_peering_routes = gcp.compute.NetworkPeeringRoutesConfig("pws-peering-routes",
    peering=pws_private_vpc_connection.peering,
    network=vpc.name,
    import_custom_routes=True,
    export_custom_routes=True,
    # Explicitly wait for the connection to finish
    opts=pulumi.ResourceOptions(depends_on=[pws_private_vpc_connection]))

### --- Firewall
gcp.compute.Firewall("allow-cloudrun-to-db",
    network=vpc.id,
    allows=[{"protocol": "tcp", "ports": ["5432"]}],
    source_ranges=[pws_cloud_run_subnet.ip_cidr_range],
    direction="INGRESS")

### --- STORAGE AND BUCKETS ---
pws_bucket_suffix = random.RandomString("pws-bucket-suffix", length=8, upper=False, special=False)
pws_static_bucket = gcp.storage.Bucket("pws-static-storage",
    name=pws_bucket_suffix.result.apply(lambda suffix: f"pws-static-assets-{suffix}"),
    location=region,
    cors=[gcp.storage.BucketCorArgs(
        # Replace with your actual portfolio subdomain
        origins=["https://yourwebsite.com", "https://www.yourwebsite.com", "https://subdomain.yourwebsite.com"],
        # GET is required for viewing files; HEAD is often used for metadata
        methods=["GET", "HEAD"],
        # Allowing standard headers like Content-Type
        response_headers=["*"],
        # How long the browser caches this CORS preflight (e.g., 1 hour)
        max_age_seconds=3600,
    )],
    force_destroy=False, # Set to False for production
    uniform_bucket_level_access=True) # Recommended for IAM-based access

### --- DATABASE: Low cost PostgreSQL instance using Cloud SQL ---
### --- Enable the Cloud SQL Admin API
pws_sql_admin_api = gcp.projects.Service("pws-sql-admin-api",
    service="sqladmin.googleapis.com",
    disable_on_destroy=False) # Recommended to prevent accidental service disruption

### --- Enable Data Access audit logs for Cloud SQL (sqladmin.googleapis.com)
pws_audit_config = gcp.projects.IAMAuditConfig("pws-db-audit-config",
    project=gcp.config.project,
    service="cloudsql.googleapis.com",
    audit_log_configs=[
        gcp.projects.IAMAuditConfigAuditLogConfigArgs(
            log_type="DATA_READ", # Logs when data is read
            # Add the service account here to stop logging its reads
            exempted_members=[sa.email.apply(lambda email: f"serviceAccount:{email}")]
        ),
        gcp.projects.IAMAuditConfigAuditLogConfigArgs(
            log_type="DATA_WRITE", # Logs when data is written
            # Add the service account here to stop logging its writes
            exempted_members=[sa.email.apply(lambda email: f"serviceAccount:{email}")]
        ),
        gcp.projects.IAMAuditConfigAuditLogConfigArgs(
            log_type="ADMIN_READ", # Logs metadata/config reads
        ),
    ])

### --- Create the Cloud SQL instance
pws_db_instance = gcp.sql.DatabaseInstance("pws-db-v1",
    database_version="POSTGRES_15",
    settings=gcp.sql.DatabaseInstanceSettingsArgs(
        tier="db-f1-micro", 
        disk_type="PD_HDD",
        disk_size=10,
        disk_autoresize=True,
        disk_autoresize_limit=20,
        availability_type="ZONAL",
        ip_configuration=gcp.sql.DatabaseInstanceSettingsIpConfigurationArgs(
            ipv4_enabled=False,  # Enable Public IP for local development access
            private_network=vpc.id,
            ssl_mode="ENCRYPTED_ONLY",
            #authorized_networks=[{
            #    "name": "my-local-machine",
            #    "value": "[insert-local-machine-ip here]/32", # Only you can connect
            #}],
        ),
        # Enable the Password Validation Policy
        password_validation_policy=gcp.sql.DatabaseInstanceSettingsPasswordValidationPolicyArgs(
            enable_password_policy=True,
            min_length=12,
            complexity="COMPLEXITY_DEFAULT", # Requires upper, lower, digit, and symbol
            reuse_interval=5,                # Cannot reuse last 5 passwords
            disallow_username_substring=True, # Password cannot contain username
        ),
        # Ensure IAM authentication is also enabled for your Cloud Run service
        database_flags=[
            gcp.sql.DatabaseInstanceSettingsDatabaseFlagArgs(
                name="cloudsql.iam_authentication",
                value="on",
            ),
            # Required for "Database Auditing" to be marked as enabled
            gcp.sql.DatabaseInstanceSettingsDatabaseFlagArgs(
                name="cloudsql.enable_pgaudit",
                value="on",
            ),
            # Specifies what to log (e.g., all, read, write, ddl)
            gcp.sql.DatabaseInstanceSettingsDatabaseFlagArgs(
                name="pgaudit.log",
                value="write,ddl,role,function", 
            ),
        ],
        deletion_protection_enabled=True, # Prevents accidental deletion of the instance (Recommended for production)
        backup_configuration=gcp.sql.DatabaseInstanceSettingsBackupConfigurationArgs(
            enabled=True,
            start_time="03:00",
            # Keep only the last 7 backups (the minimum allowed) to save costs
            backup_retention_settings=gcp.sql.DatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsArgs(
                retained_backups=7,
                retention_unit="COUNT",
            ),
        ),
    ),
    opts=pulumi.ResourceOptions(depends_on=[pws_private_vpc_connection]))

pws_db = gcp.sql.Database("pws-db", name="pws_db", instance=pws_db_instance.name)
pws_db_user = gcp.sql.User("pws-user", name="pws_admin", instance=pws_db_instance.name, password=pws_secret_versions["pws-db-password"].secret_data)

### --- CLOUD RUN SERVICE ---

### --- IAM SQL Access
gcp.projects.IAMMember("pws-sa-sql-client",
    project=gcp.config.project,
    role="roles/cloudsql.client",
    member=sa.email.apply(lambda e: f"serviceAccount:{e}"))

### --- IAM Bucket Access (Object Admin allows Read/Write/Delete)
gcp.storage.BucketIAMMember("pws-sa-bucket-admin",
    bucket=pws_static_bucket.name,
    role="roles/storage.objectAdmin",
    member=sa.email.apply(lambda e: f"serviceAccount:{e}"))

### --- Service
pws_service = gcp.cloudrunv2.Service("pws-app-v1",
    location=region,
    ingress="INGRESS_TRAFFIC_ALL",
    # Required for startup cpu boost feature
    launch_stage="BETA", 
    template=gcp.cloudrunv2.ServiceTemplateArgs(
        service_account=sa.email,
        vpc_access=gcp.cloudrunv2.ServiceTemplateVpcAccessArgs(
            network_interfaces=[{"network": vpc.id, "subnetwork": pws_cloud_run_subnet.id}],
            egress="PRIVATE_RANGES_ONLY",
        ),
        containers=[gcp.cloudrunv2.ServiceTemplateContainerArgs(
            image=f"us-central1-docker.pkg.dev/portfolio-ws-492019/pws-repo/portfolio@sha256:1442b996060d17572db91e9530dfd8e56234359375d7e3ef8aba7af06bcafe47",
            # Results in Pulumi error
            #startupCpuBoost=True, 
            resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                limits={"cpu": "1", "memory": "1Gi"},
            ),
            envs=[
                {"name": "DB_HOST", "value": pws_db_instance.private_ip_address},
                {"name": "DB_NAME", "value": pws_db.name},
                {"name": "DB_USER", "value": pws_db_user.name},
                {"name": "DB_PASS", "value": pws_secret_versions["pws-db-password"].secret_data},
                {"name": "DB_PORT", "value": "5432"},
                {"name": "GS_BUCKET_NAME", "value": pws_static_bucket.name},
                {"name": "DEBUG", "value": "False"},
            ],
        )],
        scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
            max_instance_count=10,
            min_instance_count=0,
        ),
    ))

### --- PUBLIC Access
# This makes the "anyone with the link" part work which is required for Cloud Run domain mapping or Firebase Hosting.
pws_public_iam_policy = gcp.cloudrunv2.ServiceIamMember("allow-public-access",
    name=pws_service.name,
    location=pws_service.location,
    role="roles/run.invoker",
    member="allUsers")

# Allow anyone on the internet to READ the static files
pws_public_bucket_read = gcp.storage.BucketIAMMember("static-bucket-public-read",
    bucket=pws_static_bucket.name,
    role="roles/storage.objectViewer",
    member="allUsers")

### --- FIREBASE HOSTING

### --- Ensure the Firebase API is enabled (required for Hosting)
pws_firebase_api = gcp.projects.Service("pws-firebase-api",
    service="firebase.googleapis.com",
    disable_on_destroy=False) # Recommended to prevent accidental service disruption

### --- Create a separate provider for Firebase resources since some of them require the "google-beta" API
pws_beta_provider = gcp.Provider("pws-beta-provider",
    project=project, 
    region=region)

### --- Create a Firebase Project (This is required to use Firebase Hosting, but it doesn't create any additional resources beyond what we already have in the GCP project)
pws_firebase_project = gcp.firebase.Project("pws-firebase-project",
    project=project,
    opts=pulumi.ResourceOptions(provider=pws_beta_provider,depends_on=[pws_firebase_api])) # Ensure the API is enabled before creating the Firebase project

### -- Random suffix for unique Firebase Hosting site ID (since they are global)
pws_firebase_suffix = random.RandomString("suffix",
    length=6,
    special=False,
    upper=False)

### --- Cloud Run service reference
pws_cloud_run_service = pws_service 

### -- Firebase Hosting Site with dynamic ID and routing to Cloud Run
pws_hosting_site = gcp.firebase.HostingSite("pws-hosting-site",
    project=pws_firebase_project.project,
    site_id=pulumi.Output.concat("pws-v1-", pws_firebase_suffix.result)
)

### --- Define the Hosting Version (The Routing Rules)
pws_hosting_version = gcp.firebase.HostingVersion("pws-hosting-version",
    site_id=pws_hosting_site.site_id,
    config=gcp.firebase.HostingVersionConfigArgs(
        rewrites=[gcp.firebase.HostingVersionConfigRewriteArgs(
            glob="**",
            run=gcp.firebase.HostingVersionConfigRewriteRunArgs(
                service_id=pws_cloud_run_service.name,
                region=pws_cloud_run_service.location,
            ),
        )],
    ),
)

### --- Release the Version
pws_hosting_release = gcp.firebase.HostingRelease("pws-hosting-release",
    site_id=pws_hosting_site.site_id,
    version_name=pws_hosting_version.name,
    message="PWS dynamic staging site pointing to Cloud Run"
)

### --- Map the Custom Domain (Optional for staging)
# Comment this out to test on the .web.app URL first

subdomains = ["subdomain.yourwebsite.com", ]

for domain in subdomains:
    gcp.firebase.HostingCustomDomain(f"mapping-{domain}",
        site_id=pws_hosting_site.site_id,
        custom_domain=domain)


### --- Exports
pulumi.export("pws_dynamic_site_id", pws_hosting_site.site_id)
pulumi.export("pws_firebase_url", pws_hosting_site.default_url)

