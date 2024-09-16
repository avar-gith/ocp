# file: application/urls.py

from django.contrib import admin
from django.urls import include, path
from organization.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/organization/', include('organization.urls')),
    path('api/jira/', include('jira.urls')),
    path('api/office/', include('office.urls')),
    path('', index, name='index'),
]
