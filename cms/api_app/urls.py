from django.urls import path
from api_app import views

urlpatterns = [
    path('users/', views.create_user),
    path('users/<int:user_id>/', views.get_user),
    path('users/<int:user_id>/update/', views.update_user),
    path('users/<int:user_id>/delete/', views.delete_user),

    path('posts/', views.create_post),
    path('posts/<int:post_id>/', views.get_post),
    path('posts/<int:post_id>/update/', views.update_post),
    path('posts/<int:post_id>/delete/', views.delete_post),

    path('like/', views.create_like),
    path('likes/<int:like_id>/', views.get_like),
    path('like/<int:like_id>/update/', views.update_like),
    path('likes/<int:like_id>/delete/', views.delete_like),

    path('posts/all/', views.get_all_posts),
]