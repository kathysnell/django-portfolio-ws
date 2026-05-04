from django.db import models
from tinymce.models import HTMLField
from django.utils.html import strip_tags
from colorfield.fields import ColorField
import nh3
from django.utils.safestring import mark_safe
import os
from django.core.files.storage import default_storage
from .storage import NoSuffixStorage
from .utils import save_webp

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def get_upload_path(instance, filename):
    return f'{filename}'

class BaseImage(models.Model):
    # Use the dynamic path function here
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True, storage=NoSuffixStorage(), verbose_name="Image") 
   
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.image:
            file_path = os.path.join(self.upload_folder, self.image.name)
            default_storage.save(file_path, self.image)
            super().save(*args, **kwargs)
            save_webp(file_path)             

class WebpOrLegacyBackgroundImage(BaseImage):
    upload_folder = 'backgrounds'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('image').verbose_name = "Background Image"

    def __str__(self):
        if self.image:
            return f"Image: {self.image.name.split('/')[-1]}"
        return f"Empty Image (ID: {self.id})"

class BaseContent(BaseModel):
    content = HTMLField()
    bgcolor = ColorField(default='#ffffff', verbose_name="Background Color")
    bgimage = models.ForeignKey(
        WebpOrLegacyBackgroundImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_related" # Necessary for abstract inheritance
    )
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
        # Define what tags/attributes TinyMCE should allow
        self.content = nh3.clean(
            self.content,
            
            tags={
                "p", "b", "i", "u", "em", "strong", "a", "img", 
                "ul", "ol", "li", "br", "h1", "h2", "h3", "span", "picture", "source"
            },
            attributes={
                "a": {"href", "title", "target"},
                "img": {"src", "alt", "width", "height"},
                "picture": {"source"},
                "source": {"srcset", "type"},
                "*": {"style"}
            },
            

            link_rel="noopener noreferrer" # Recommended for security
        )        
        super().save(*args, **kwargs)
    
    @property
    def content_html(self):
        return mark_safe(self.content)
    
    class Meta:
        abstract = True