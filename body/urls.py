from django.urls import path

from link.context_processors import get_global_links

from . import views
from django.conf import settings

urlpatterns = [
    path('', views.BodyListView.as_view(), name='body-list'),
]

links = get_global_links()
# Add URL patterns for internal links defined in the database
if links:
    for link in links:
        if link.page and link.is_internal_url():
            urlpatterns.append(path(f'{link.page}/', views.body_detail, name=f'body'))

from django.conf import settings
from django.conf.urls.static import static
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
