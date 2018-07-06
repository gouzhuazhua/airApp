"""airApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from air import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.test),
    path('register/', views.register),
    path('login/', views.login),
    path('update_apps/', views.update_steam_apps),
    path('update_news/', views.update_steam_news),
    path('news/', views.get_steam_news_from_db),
    path('owned_games/', views.get_player_ownedgames_from_db),
    path('recently_games/', views.get_player_recentlygames_from_db),
    path('player_bans/', views.get_player_bansbyname_from_api),
    path('player_bans_query/', views.get_player_bansbyid_from_api),
    path('player_summaries/', views.get_player_summaries_from_db),
]
