"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from manager import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.login),
    path('index',views.logins),
    path('regi',views.regist),
    path('index1',views.returnindex),
    path('photo',views.photo),
    path('family',views.family),
    path('shanchu1',views.delete1),
    path('shipin',views.shipin),
    path('p2p',views.p2p),
    path('map',views.map),
    path('message',views.message),
    path('beiwang',views.beiwang),
    path('xiangqing',views.xiangqing),
    path('describ',views.describ),
    path('xinwen',views.new),
    path('shangchuan',views.shangchuan),
    path('yuyin',views.yuyin),
    path('fanhui',views.family),
]
