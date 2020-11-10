"""lvanops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from lvanapi import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', views.index),
    url(r'^game_iptables_check/', views.game_iptables_check),
    url(r'^login_iptables_check/', views.login_iptables_check),
    url(r'^game_check/', views.game_check),
    url(r'^login_check/', views.login_check),
    url(r'^ver/', views.ver),
    url(r'^cron/', views.cron),
    url(r'^update/', views.update),
    url(r'^hostinfo/api/', views.hostinfo_api),
    url(r'^host/', views.host),
    url(r'^iptables', views.iptables),
    url(r'^/*',views.login),
]
