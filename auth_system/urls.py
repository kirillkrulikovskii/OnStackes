from django.urls import path

from .models import *
from .views  import *

app_name = 'auth_system'

urlpatterns = [
    path('register-login/', register_login, name='register_login'),
    path('profile/<int:pk>/', profile_view, name='profile'),
]