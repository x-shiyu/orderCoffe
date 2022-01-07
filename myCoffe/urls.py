from django.contrib import admin
from django.urls import path, include
from .views import index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/file/', include('apps.File.urls')),
    path('api/auth/', include('UserInfo.urls')),
    path('api/user/', include('UserInfo.urls')),
    path('api/goods/', include('apps.Goods.urls')),
    path('api/order/', include('apps.Order.urls')),
    path('api/shop/', include('apps.Goods.urls')),
    path('api/cate/', include('apps.Goods.urls')),
    path('api/charts/', include('apps.Goods.urls')),
]
