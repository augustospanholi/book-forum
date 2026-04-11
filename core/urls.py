from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('our-history/', views.our_history, name='our_history'),
    path('contact/', views.contact, name='contact'),
]