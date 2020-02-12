from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils import timezone 

from portal.decorators import need_login
from portal import functions as func
from portal.models import Usuari, Registre

import os
import requests
import signal

# Views here.

def login(request):
  ip = func.get_client_ip(request)
  try:
    r = Registre.objects.get(ip=ip)
    return redirect('resources')
  
  except:
    if request.method == 'GET':
      return render(request, 'login.html')

    elif request.method == 'POST':
      nom = request.POST.get('fname', '')
      cognom = request.POST.get('lname', '')
      lloc_r = request.POST.get('lloc_r', '')
      sexe = request.POST.get('sexe', '')
      email = request.POST.get('email', '')
      edat = request.POST.get('edat', '')

      ip = func.get_client_ip(request)
      try:
        # Adding entry with ip registred
        r = Registre(ip=ip)
        r.save()
        try:
          # Send signal to fakeDNS.pid to make him update ip_table
          os.system("sudo " + settings.BASE_DIR + '/updateIP')
        except Exception as e:
          print("Error enviant signal a fakeDNS: ", e)
          pass
      except Exception as e:
        print("Error registrant ip: " + e)

      u = Usuari(nom=nom, cognom=cognom, edat=edat, resideix_a=lloc_r, sexe=sexe, email=email)
      u.save()
      return redirect('/resources/')

def home(request):
    if request.method == 'GET':
      return redirect('login')

def resources(request):
    if request.method == 'GET':
        return render(request, 'index.html')

@login_required()
def retrieve_canvi_contrasenya(request):
  if request.method == 'POST':
    user = request.POST.get('user')
    passwd = request.POST.get('passwd')
    nou = {user:passwd}
    settings.BASICAUTH_USERS = nou

@login_required()
def retrieve_frontend(request):
  if request.method == 'GET':
    return render(request,'statistics.html')


@login_required()
def retrieve(request):
    if request.method == "GET":
      dia = timezone.now().day
      mes = timezone.now().month
      aany = 2019
      date = list([aany,mes,dia])
      if 'date' in request.GET:
        date = request.GET['date'].split('-')
      data = timezone.datetime(int(date[0]), int(date[1]), int(date[2]))
      file_path='/tmp/usuaris.csv'
      Usuari.objects.filter(registrat__gt = data).extra(
        select={
          'Prénom': 'nom',
          'Nom': 'cognom',
          'Email': 'email',
          'Âge': 'edat',
          'Sexe': 'sexe',
          'Lieu de résidence': 'resideix_a',
          'Date de connexion': 'registrat'

        }
      ).values(
        'Prénom', 'Nom', 'Email', 'Âge', 'Sexe', 'Lieu de résidence', 'Date de connexion'
      ).to_csv(file_path)
      with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/csv")
        response['Content-Disposition'] = 'inline; filename=usuaris.csv' 
        return response
      return HttpResponse(status=404)

def view_404(request, exception=None):
  return redirect('login')

def toogle(request):
  func.toogle_router()
  return redirect('statistics')
