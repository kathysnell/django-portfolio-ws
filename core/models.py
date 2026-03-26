from django.db import models
from tinymce.models import HTMLField
from django.utils.html import strip_tags
from colorfield.fields import ColorField

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseContent(BaseModel):
    content = HTMLField()
    bgcolor = ColorField(default='#ffffff')
    bgimage = models.ImageField(upload_to='backgrounds/', null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return len(self.content) > 15 and strip_tags(self.content)[:15] or strip_tags(self.content)

    class Meta:
        abstract = True