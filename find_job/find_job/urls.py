from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from scraping.views import (index, list_view, view_detail, ViewDetail,
                            ViewCreate, ViewUpdate, ViewDelete)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', list_view, name='list'),
    path('', include('scraping.urls', namespace='scraping')),
    path('users/', include(('users.urls', 'users'))),
    path('detail/<int:pk>/', ViewDetail.as_view(), name='detail'),
    path('create/', ViewCreate.as_view(), name='create'),
    path('update/<int:pk>/', ViewUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', ViewDelete.as_view(), name='delete'),
    path('', index, name='index'),
]
