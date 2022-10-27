from django.urls import path
from users.views import (login_view, logout_view, register_view, update_view,
                         delete_view, contact)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', register_view, name='registration'),
    path('update/', update_view, name='update'),
    path('delete/', delete_view, name='delete'),
    path('contact/', contact, name='contact'),
]
