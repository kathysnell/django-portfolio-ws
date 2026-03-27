from core.models import BaseContent, BaseModel
from django.db import models

class Link(BaseContent):
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    text = models.CharField(max_length=15, blank=True)
    url = models.URLField(blank=True)

class LinkBar(BaseContent):
    position = models.CharField(max_length=30, choices=[('pre_header', 'Before Header (intro)'),
                                                        ('post_header', 'After Header (intro)'),
                                                        ('post_card', 'After Flash Card'),
                                                        ('pre_footer', 'Before Page Footer')],
                                                        default='pre_footer')
    justify = models.CharField(max_length=30, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], default='center')

