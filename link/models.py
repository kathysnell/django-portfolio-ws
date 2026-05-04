from core.models import BaseContent
from django.db import models
from django.urls import resolve, Resolver404
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

class Link(BaseContent):
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    text = models.CharField(max_length=15, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.text or self.url or super().__str__() + f"Active: {self.active}"    
        

class LinkBar(BaseContent):
    position = models.CharField(max_length=30, choices=[('pre_header', 'Before Header (intro)'),
                                                        ('post_header', 'After Header (intro)'),
                                                        ('post_card', 'After Flash Card'),
                                                        ('pre_footer', 'Before Page Footer')],
                                                        default='pre_footer')
    justify = models.CharField(max_length=30, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], default='center')

    def __str__(self):
        return f"Link Bar ({self.position}, {self.justify}) Active: {self.active}"

