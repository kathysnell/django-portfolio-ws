from django.contrib import admin
from .models import Link, LinkBar

class LinkAdmin(admin.ModelAdmin):
    exclude = ('content','page',)

class LinkBarAdmin(admin.ModelAdmin):
    exclude = ('content','page',)

admin.site.register(Link, LinkAdmin)
admin.site.register(LinkBar, LinkBarAdmin)
