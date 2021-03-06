from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerPage, name='signup'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile')
]
