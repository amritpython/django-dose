"""dose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path

from shopify_app.views import  callback, LoginView, uninstall 
from home.views import HomeView
from shopify_app.views import orders_create
from home import urls

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('auth/shopify/callback', callback, name='callback'),
    path('uninstall', uninstall, name='uninstall'),
    path('orders_create', orders_create, name='orders_create'),
    path('', HomeView.as_view(), name='root_path'),
    path('',include('home.urls')),
    path('djangoadmin/', admin.site.urls),
]

