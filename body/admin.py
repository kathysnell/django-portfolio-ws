from django.contrib import admin
from .models import Card, CardSide, BodyContent

class CardSideInline(admin.StackedInline):
    model = CardSide
    extra = 2      # Show two forms (one for Front, one for Back)
    max_num = 2    # Don't allow more than two sides
    can_delete = False 

class CardAdmin(admin.ModelAdmin):
    exclude = ('box','content')
    inlines = [CardSideInline]

class BodyContentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Card, CardAdmin)
admin.site.register(BodyContent, BodyContentAdmin)
