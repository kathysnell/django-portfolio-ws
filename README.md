# django-portfolio-ws
An portfolio website model featuring dynamic display of content from a Postgres database. This model is a low code solution, ideal for professionals who want to easily develop and update a professional portfolio. The website is built using Django, deployed as a Google Cloud Run service and hosted by Firebase. It includes a custom admin interface for managing pages, and uses TinyMCE for rich HTML content.

## Project Preparations
Clone the repository: 
```bash 
git clone https://github.com/kathysnell/django-portfolio-ws.git
```
Navigate to the project directory: 
```bash
cd django-portfolio-ws
```
Create a virtual environment: 
```bash
python -m venv venv
```
Activate the virtual environment (Linux/Mac): 
```bash
source venv/bin/activate
```
or (Windows)
```bash
venv\Scripts\activate
```
Install the required dependencies: 
```bash
pip install -r requirements.txt
```

## Local Development (sqlite3 for local development)
Apply migrations: 
```bash
python manage.py migrate
```
Create a superuser: 
```bash
python manage.py createsuperuser
```
Run the development server: 
```bash
python manage.py runserver
```
Access the application at 
```bash
http://localhost:8000/
```

## Local Development (PostgreSQL with Docker Compose)
Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

Clone the repository: 
```bash
git clone https://github.com/kathysnell/django-portfolio-ws.git
```
Navigate to the project directory: 
```bash
cd django-portfolio-ws
```
Ensure Postgres database is enabled in portfolio_ws_project.settings.py
Build the Docker image: 
```bash
./dockerBuild.sh
```
In another terminal, run Docker Compose to start the application: 
```bash
docker-compose up
```
Apply migrations inside the running container: 
```bash
docker exec -it <container_name> python manage.py migrate
```
Create a superuser inside the running container: 
```bash
docker exec -it <container_name> python manage.py createsuperuser
```
Access the application at:
```bash
http://localhost:8080/
```

## Google Cloud Run Development
Create a .env file based upon .env-example
Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
Authenticate with Google Cloud: 
```bash
gcloud auth login
```
Set the project: 
```bash
gcloud config set project <your-project-id>
```
Create the following components in Google Cloud:
   - Cloud SQL instance with PostgreSQL database, **allowing an external connection with your ip address only**
   - Cloud Storage bucket for static files

Navigate to the project directory: 
```bash
cd django-portfolio-ws
```
Uncomment and set the following items in .env:
   - Set GS_BUCKET_NAME to the cloud storage bucket name created.
   - Set DB_NAME to the cloud sql datbase name
   - Set DB_HOST to 127.0.0.1
   - If prompted set DB_USER and DB_PASS as configured in GCP.

Ensure Postgres database is enabled in portfolio_ws_project.settings.py

Install the Google Cloud SQL proxy: 
```bash
brew install cloud-sql-proxy
```
Run the SQL proxy: 
```bash
./cloud-sql-proxy <PROJECT_ID:REGION:INSTANCE_ID>
```
Open another terminal on the project level:
```bash
cd django-portfolio-ws
```
Start the virtual environment: 
```bash
source venv/bin/activate
```
Run migrations: 
```bash
python manage.py migrate
```
Collect static files on the bucket: 
```bash
python manage.py collectstatic
```
Run server: 
```bash
python manage.py runserver
```
Access the application at 
```bash
http://localhost:8000/
```

## Personalization
To personalize the portfolio website, please modify the following files:
- `core/contants.py`
- `static/templates/robots.txt`
- `static/templates/sitemap.xml`
- add customized icon files to `static/images` directory

If hosting on Firebase add the following customized files to the `public` directory:
- `robots.txt`
- `sitemap.xml`
- customized icon files
- customized `404.html` file

## Website construction
- With the server running, navigate to the website's ADMIN_PATH (example `https://yourwebsite.com/your-admin-path/)
- Enter superuser credentials
- The following elements are available for constructing webpages:
    - **INTRO** serves as the Heading for all webpages
    - **BODY** serves as the content on a specific webpage
        - Card is a flipping card (front / back), that is created for a designated page 
        - Body contents is a html area that is created for a designated page 
    - **LINK**
        - Link Bars hold a set of Links horizontally
        - Links represent an image and/or text that transistions to another page on the portfolio website.
- The following configuration items are enabled as applicable for each of the webpage elements listed above.
    - **HTML Content:** Hosted by TinyMCE
    - **Background Color:** Desired color for web page background.
    - **Background Image:** Desired image for web page background.
    - **Active:** Only functional when active is checked. This allows elements to be quickly added or removed.
    - **Page:** Specify path within domain, leaving blank for main page elements.
- **Card** specific configuration items:
    - **Rounded Corners:** Enable for rounded corners on configured card.
    - **CardSide:** Specific configuration for front and back of Card.
        - **Is front:** enable one side as front
        - **Border Color:** specify color of border of each side
- **LinkBar** specific configuration items:
    - **Position:** Select according to desired postion of link bar on webpage.
    - **Justify:** Select according to desired justification of link bar on webpage.
- Link specific configuration items:
    - **Icon:** Picture to use for link, if any.
    - **Text:** Text to use for link.
    - **Url:** Fully qualified url for the target page. Be sure to configure a Body Content item with the Page configuration for the path portion of the url.

## GCP Deployment
- Example Pulumi Python code can be found at `pulumi_gcp_example/__main__.py`
- Set DEBUG in .env to False

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Resources
- Google Cloud Platform (GCP): https://cloud.google.com 
- Pulumi: https://pulumi.com
- TinyMCE HTML Content: https://www.tiny.cloud

