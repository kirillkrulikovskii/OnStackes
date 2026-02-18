from django.urls import path

from .models import *
from .views import register_login_views, profile_view, logout_view, edit_profile_view

app_name = 'auth_system'

urlpatterns = [
    path('reg/'         , register_login_views, name='signup'      ),
    path('profile/'     , profile_view        , name='profile'     ),
    path('logout/'      , logout_view         , name='logout'      ),
    path('edit-profile/', edit_profile_view   , name='edit_profile'),
]