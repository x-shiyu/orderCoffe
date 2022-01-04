from django.urls import path, include
from .views import upload,getFile


urlpatterns = [
    path('upload/',upload, name='upload'),
    path('fetch/',getFile, name='getFile'),
]
