from django.urls import path
from .views import tinymce_upload_image

app_name = 'core'

urlpatterns = [
    path('upload-image/', tinymce_upload_image, name='tinymce_upload'),
]
