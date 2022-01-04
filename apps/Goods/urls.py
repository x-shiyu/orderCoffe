from django.urls import path, include
from .views import CateView,GoodsView


urlpatterns = [
    path('cate/',CateView.as_view(), name='cate'),
    path('list/',GoodsView.as_view(), name='goods-list'),
]
