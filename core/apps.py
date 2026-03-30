from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.contrib import admin
        from django.contrib.auth.models import User, Group        
        # use try/except to prevent errors if they are already unregistered
        try:
            admin.site.unregister(User)
            admin.site.unregister(Group)
        except admin.sites.NotRegistered:
            pass
