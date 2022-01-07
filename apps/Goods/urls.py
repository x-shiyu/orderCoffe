from django.urls import path, include
from .views import CateView,GoodsView,ShopGoodsView,GoodsDeleteView,CateDeleteView
from .charts import ChartsView

urlpatterns = [
    path('cate/',CateView.as_view(), name='cate'),
    path('list/',GoodsView.as_view(), name='goods-list'),
    path('goods/',ShopGoodsView.as_view(), name='shop-goods'),
    path('delete/',GoodsDeleteView.as_view(), name='goods-action'),
    path('remove/',CateDeleteView.as_view(), name='cate-action'),
    path('info/',ChartsView.as_view(), name='charts'),
]
