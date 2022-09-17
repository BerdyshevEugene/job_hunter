from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from find_jobs. views import index, list_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('find_jobs.urls', namespace='find_jobs')),
    path('list', list_view, name='list'),
    path('', index, name='index'),

]
