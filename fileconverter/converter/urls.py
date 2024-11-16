from django.urls import path
from . import views
from django.urls import path
from .views import convert_file, download_file
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='convert'),
    path('about/', views.about_view, name='about'),  
    path('service/', views.service_view, name='service'),  
    path('why/', views.why_view, name='why'),  
    path('team/', views.team_view, name='team'), 
    path('convert/', views.convert_view, name='convert'),
    path('convert/', convert_file, name='convert_file'),
    path('download/<str:file_name>/', download_file, name='download_file'),
]



from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
