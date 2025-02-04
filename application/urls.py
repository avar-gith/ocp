# file: application/urls.py

from django.contrib import admin
from django.urls import include, path
from organization.views import index
from organization.views import index, life_view
from adan import views


urlpatterns = [
    path('', index, name='index'),
    path('adan/', include('adan.urls')),
    path('office/', include('office.urls')),
    path('organization/', include('organization.urls')),
    
    path('admin/', admin.site.urls),
   
    path('api/organization/', include('organization.urls')),
    path('api/jira/', include('jira.urls')),
    path('api/office/', include('office.urls')),
    
    path('life/', life_view, name='life'),
    
    path('api/active_model/', views.ActiveModelListView.as_view(), name='active-models'),
    path('api/', views.api_list_view, name='api_list'),
]
