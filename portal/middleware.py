from portal import functions as func
from portal import models
from portal import views 

from django.shortcuts import render, redirect
import re


class SimpleMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response
    # One-time configuration and initialization.

  def __call__(self, request):
    # We use this method to check if ip from request is logged before
    # line `response = self.get_response(request)`
    # If 
    #   present in bd or 
    #   wants an admin page or
    #   wants /login: 
    #        pass
    # Else: redirect to login

    adm_or_login = "(^/adm/|^/login)"
    if re.match(adm_or_login, request.path) is None:
      IP = func.get_client_ip(request)
      try:
        r = models.Registre.objects.get(ip=IP)
      except Exception as e:
        return redirect('login')

    response = self.get_response(request)

    # Code to be executed for each request/response after
    # the view is called.

    return response 


