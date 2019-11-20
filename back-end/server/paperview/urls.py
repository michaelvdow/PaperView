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

    # Test paths, delete these eventually
    path('listnames/', views.listnames, name='listnames'),
    path('echopostdata/', views.echopostdata, name='echopostdata'),
    path('tothelimit/', views.tothelimit, name='tothelimit'),
    path('addname/', views.addname, name='addname'),
    path('search/test/', views.searchForName, name='search_test'),
    path('graphtest', views.graphTest, name='Graph test'),
    # End of test paths

    path('search/author', views.search_for_author, name = 'search_for_author'),
    path('search/article', views.search_for_article, name = 'search_for_article'),
    path('search/interest', views.search_for_interest, name = 'search_for_interest'),
	path('author/<int:authorid>', views.specific_author, name = 'specific_author'),
    path('article/<int:articleid>', views.specific_article, name = 'specific_article'),
    path('new/author/', views.new_author, name = 'new_author'),
    path('new/article/', views.new_article, name = 'new_article'),
]
