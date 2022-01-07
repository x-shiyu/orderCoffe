from os import name
from django.urls import path, include
from .views import RegisterView, LoginView,UserView,ShopView,LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('info/', UserView.as_view(),name='user-info'),
    path('shop/', ShopView.as_view(),name='shop-info')
]
