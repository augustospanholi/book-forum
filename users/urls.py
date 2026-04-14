from django.urls import path
from users.views import login, register, logout, banned

urlpatterns = [
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
    path('banned', banned, name='banned'),
]