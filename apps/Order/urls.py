from django.urls import path, include
from .views import OrderView


urlpatterns = [
    path('list/',OrderView.as_view(), name='order-list'),
]
