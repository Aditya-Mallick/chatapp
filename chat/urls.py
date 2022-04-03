from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logoutPage, name='logout'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('delete/<str:pk>/', views.delete, name='delete'),
    path('profile/<str:pk>/', views.profile, name='profile')
]

