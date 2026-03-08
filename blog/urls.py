from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('fetch_comments/<int:pk>/', views.fetch_comments, name='fetch_comments'),
    # path('post_list/'      , views.PostListView.as_view()  , name='post_list'  ),
    # path('<int:pk>/'       , views.PostDetailView.as_view(), name='post_detail'),
    path('create/'         , views.create_post             , name='create_post'),
    path('<int:pk>/edit/'  , views.edit_post               , name='edit_post'  ),
    path('<int:pk>/delete/', views.delete_post             , name='delete_post'),
]