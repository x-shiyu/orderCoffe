"""myCoffe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls.conf import include
# from apps.coffeOrderClient import apis as coffeOrderClientAPI
# from apps.coffeOrderAdmin import apis as coffeOrderAdminAPI
# from apps.coffeOrderBusiness import apis as coffeOrderBusinessAPI
# from apps.coffeOrderClient import urls as coffeOrderClientURL
# from apps.coffeOrderAdmin import urls as coffeOrderAdminURL
# from apps.coffeOrderBusiness import urls as coffeOrderBusinessURL
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('myCoffe.apps.coffeOrderClient.urls')),
    path('', include('myCoffe.apps.coffeOrderClient.urls')),
]
