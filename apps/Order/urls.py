from django.urls import path, include
from .views import upload


urlpatterns = [
    path('upload/',upload, name='upload'),
]
