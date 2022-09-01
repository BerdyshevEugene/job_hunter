from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from . views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('find_jobs.urls', namespace='find_jobs')),
    path('home/', home),
]
