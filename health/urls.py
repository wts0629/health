"""blogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from main import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='main'),
    path('login',views.v_login,name='main'),
    path('logout',views.v_logout,name='main'),
    path('register',views.register,name='main'),
    path('record',views.record,name='main'),
    path('history',views.history,name='main')
]

# url(r'^static/(?P<path>.*)$', static.serve,
#         {'document_root': settings.STATIC_ROOT}, name='static')  # 解决静态文件加载失败问题
