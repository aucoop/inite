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
from portal import public_views
from portal import proxy 

urlpatterns = [
    # URL's for admin pages
url(r'^user/login',                  auth_views.LoginView.as_view(),               name="user_login"),
url(r'^user/logout',                 auth_views.LogoutView.as_view(),              name="user_logout"),
url(r'^user/change_password-done$',  auth_views.PasswordChangeDoneView.as_view(),  name="user_cahnge_password_done"),
url(r'^toogle$',                    public_views.toogle,                          name='toogle'),
url(r'^retrieve$',                  public_views.retrieve,                        name='retrieve'),
url(r'^user/change_password$',
    auth_views.PasswordChangeView.as_view(template_name = 'statistics.html',
                                          form_class    =  SetPasswordForm,
                                          success_url   =  '/user/change_password-done'),
    name = "user_change_password"),

url(r'^resources$',     public_views.resources,          name='resources'),
url(r'^registration$',  public_views.registration,       name='registration'),
url(r'^statistics$',    public_views.retrieve_frontend,  name='statistics'),

    # URL's for proxy pass
url(r'^wkoff/(?P<url>.*)$',     proxy.WikiProxy.as_view(),    name='proxy'),
url(r'^mdl/(?P<url>.*)$',       proxy.MoodleProxy.as_view(),  name='proxy'),
url(r'^kacademy/(?P<url>.*)$',  proxy.KhanProxy.as_view(),    name='proxy'),
url(r'^policy$',                public_views.policy,          name='policy'),
url(r'.*',                      public_views.view_404,        name='view_404'),
]
