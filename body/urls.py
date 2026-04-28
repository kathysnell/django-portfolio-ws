from django.urls import path

from link.context_processors import global_links

from . import views
from django.conf import settings

urlpatterns = [
    path('', views.BodyListView.as_view(), name='body-list'),
]

from django.conf import settings
from django.conf.urls.static import static
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.append(path('<path:slug>/', views.dynamic_page_router, name='dynamic_page'))
