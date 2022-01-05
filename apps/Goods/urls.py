from django.urls import path, include
from .views import CateView,GoodsView,ShopGoodsView


urlpatterns = [
    path('cate/',CateView.as_view(), name='cate'),
    path('list/',GoodsView.as_view(), name='goods-list'),
    path('goods/',ShopGoodsView.as_view(), name='shop-goods'),
]
