from django.contrib import admin
from .models import Link, LinkBar

class LinkAdmin(admin.ModelAdmin):
    pass

class LinkBarAdmin(admin.ModelAdmin):
    exclude = ('content',)

admin.site.register(Link, LinkAdmin)
admin.site.register(LinkBar, LinkBarAdmin)
