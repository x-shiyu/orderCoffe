from django.urls import path, include
from .views import RegisterView, LoginView,LogoutView,UserInfo,updatePwd


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('detail/', UserInfo.as_view(),name='user_info'),
    path('password/', updatePwd),
]
