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
from django.contrib.auth.forms import SetPasswordForm
from django.urls import path
from django.conf.urls import url
from portal import views as PortalViews
from portal import proxy 

urlpatterns = [
    # URL's for admin pages
    url(r'^adm/login', auth_views.LoginView.as_view(), name="adm_login"),
    url(r'^adm/logout', auth_views.LogoutView.as_view(), name="adm_logout"),
    url(r'^adm/change_password$', auth_views.PasswordChangeView.as_view(template_name='statistics.html', form_class= SetPasswordForm, success_url='/adm/change_password-done'), name="adm_change_password"),
    url(r'^adm/change_password-done$', auth_views.PasswordChangeDoneView.as_view(), name="adm_cahnge_password_done"),

    url(r'^resources$', PortalViews.resources, name='resources'),
    url(r'^login$', PortalViews.login, name='login'),
    url(r'^toogle$', PortalViews.toogle, name='toogle'),
    url(r'^chpasswd$', PortalViews.retrieve_canvi_contrasenya, name='chpasswd'),
    url(r'^statistics$', PortalViews.retrieve_frontend, name='statistics'),
    url(r'^retrieve$', PortalViews.retrieve, name='retrieve'),
    # URL's for proxy pass
    url(r'^wkoff/(?P<url>.*)$',  proxy.WikiProxy.as_view(), name='proxy'), 
    url(r'^mdl/(?P<url>.*)$',  proxy.MoodleProxy.as_view(), name='proxy'), 
    url(r'^kacademy/(?P<url>.*)$',  proxy.KhanProxy.as_view(), name='proxy'),
    url(r'^policy$', PortalViews.policy, name='policy'),
    url(r'.*', PortalViews.view_404, name='view_404'),
]

