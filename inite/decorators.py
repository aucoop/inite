from portal import functions as func
#from portal.models import Usuari, Registre
#from portal.views import login
import portal
from django.shortcuts import render, redirect

def need_login(function):
    def wrap(request, *args, **kwargs):
        ip = func.get_client_ip(request)
        try:
          r = Registre.objects.get(ip=ip)
          return function(request, *args, **kwargs)
        except:
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


  
