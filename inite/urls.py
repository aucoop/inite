"""inite URL Configuration

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
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url
from portal import views as PortalViews
from portal import proxy 

urlpatterns = [
    url(r'^adm/login', auth_views.LoginView.as_view(), name="adm_login"),
    url(r'^resources$', PortalViews.resources, name='resources'),
    url(r'^login$', PortalViews.login, name='login'),
    url(r'^chpasswd$', PortalViews.retrieve_canvi_contrasenya, name='chpasswd'),
    url(r'^debug$', PortalViews.debug, name='debug'),
    url(r'^statistics$', PortalViews.retrieve_frontend, name='statistics'),
    url(r'^retrieve$', PortalViews.retrieve, name='retrieve'),
    url(r'^wikipedia$',  proxy.WikiProxy.as_view(), name='proxy'), 
    url(r'^moodle$',  proxy.MoodleProxy.as_view(), name='proxy'), 
    url(r'^khanacademy$',  proxy.KhanProxy.as_view(), name='proxy'), 
    url(r'.*', PortalViews.view_404, name='view_404'),
]

