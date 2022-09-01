from django.urls import path
from . import views

app_name = 'find_jobs'

urlpatterns = [
    path('', views.index, name='index'),
]