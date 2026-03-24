from django.contrib import admin
from .models import Intro

class IntroAdmin(admin.ModelAdmin):
    pass

admin.site.register(Intro, IntroAdmin)
