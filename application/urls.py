# file: application/urls.py

from django.contrib import admin
from django.urls import include, path
from organization.views import index
from adan import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('adan/', include('adan.urls')),
    path('', index, name='index'),
   
    path('api/organization/', include('organization.urls')),
    path('api/jira/', include('jira.urls')),
    path('api/office/', include('office.urls')),
    
    path('api/', views.api_list_view, name='api_list'),
]
