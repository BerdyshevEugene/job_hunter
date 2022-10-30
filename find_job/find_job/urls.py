from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from scraping.views import index, list_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', list_view, name='list'),
    path('', include('scraping.urls', namespace='scraping')),
    path('users/', include(('users.urls', 'users'))),
    path('', index, name='index'),
]
