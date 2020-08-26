from portal import functions as func
from portal import models
from portal import public_views 

from django.shortcuts import render, redirect

def need_login(function):
    def wrap(request, *args, **kwargs):
        IP = func.get_client_ip(request)
        try:
          r = models.Registre.objects.get(ip=IP)
          return function(request, *args, **kwargs)
        except Exception as e:
          return redirect('login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

#def authorization(function):
#  def wrap(request, *args, **kwargs):
#     
#  wrap.__doc__ = function.__doc__
#  wrap.__name__ = function.__name__
#  return wrap


  
