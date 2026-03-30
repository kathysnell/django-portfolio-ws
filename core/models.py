from django.db import models
from tinymce.models import HTMLField
from django.utils.html import strip_tags
from colorfield.fields import ColorField
import nh3
from django.utils.safestring import mark_safe

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
    page = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        page_name = self.page if self.page else "Default"
        return self.get_short_name() + f" (Page: {page_name}, Active: {self.active})"
    
    def get_short_name(self):
        content = self.content
        if len(content) > 15:
            return strip_tags(content)[:15] + "..."
        return strip_tags(content)
    
    def save(self, *args, **kwargs):
        # Define what tags/attributes you want to allow from TinyMCE
        # This prevents users from injecting <script> or inline styles
        self.content = nh3.clean(
            self.content,
            tags={
                "p", "b", "i", "u", "em", "strong", "a", "img", 
                "ul", "ol", "li", "br", "h1", "h2", "h3"
            },
            attributes={
                "a": {"href", "title", "target"},
                "img": {"src", "alt", "width", "height"},
            },
            link_rel="noopener noreferrer" # Recommended for security
        )
        super().save(*args, **kwargs)

    @property
    def content_html(self):
        return mark_safe(self.content)
    
    class Meta:
        abstract = True