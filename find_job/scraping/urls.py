from django.urls import path
from . import views

app_name = 'scraping'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_view, name='list'),
]