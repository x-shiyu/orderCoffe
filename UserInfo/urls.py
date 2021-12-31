from os import name
from django.urls import path, include
from .views import RegisterView, LoginView,getUserInfo


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('info/', getUserInfo,name='user-info')
]
