from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:post_id>/pin/', views.pin_post, name='pin_post'),
    path('posts/<int:post_id>/resolve/', views.resolve_post, name='resolve_post'),
    path('replies/<int:reply_id>/edit/', views.reply_edit, name='reply_edit'),
    path('replies/<int:reply_id>/delete/', views.reply_delete, name='reply_delete'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/ban/', views.ban_user, name='ban_user'),
    path('rules/', views.rules, name='rules'),
    path('rules/edit/', views.rules_edit, name='rules_edit'),
    path('our-history/', views.our_history, name='our_history'),
    path('contact/', views.contact, name='contact'),
]
