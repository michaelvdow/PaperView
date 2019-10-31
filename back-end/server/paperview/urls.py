"""paperview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),   # Don't touch this, pregenerated
    path('', views.index, name='index'),
    path('listnames/', views.listnames, name='listnames'),
    path('echopostdata/', views.echopostdata, name='echopostdata'),
    path('tothelimit/', views.tothelimit, name='tothelimit'),
    path('addname/', views.addname, name='addname'),
    path('search/test/', views.searchForName, name='search_test'),
]
