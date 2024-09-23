"""Url imports"""
from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/', views.view_profile, name='profile'),
    path(
        "delete_account/<int:pk>/delete", views.profile_delete, name="profile-delete"
    ),
    path(
        'user/wishlist_add/<str:pk>/',
        views.add_remove_wishlist_items,
        name="manage-wishlist",
    ),
    path('user/<int:pk>/wishlist/', views.my_wishlist, name='my-wishlist'),
]
