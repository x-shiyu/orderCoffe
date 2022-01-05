from os import name
from django.urls import path, include
from .views import RegisterView, LoginView,UserView,ShopView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('info/', UserView.as_view(),name='user-info'),
    path('shop/', ShopView.as_view(),name='shop-info')
]
