from django.shortcuts import render, redirect
from django.db.models import F
from basicauth.decorators import basic_auth_required
from django.http import HttpResponse, HttpResponseNotFound
import requests
from portal import functions as func
from portal.models import Usuari, Registre
from inite.decorators import need_login
import os
import signal
import datetime

# Create your views here.

def login(request):
  ip = func.get_client_ip(request)
  try:
    r = Registre.objects.get(ip=ip)
    return redirect('resources')
  
  except:
    
    if request.method == 'GET':
      return render(request, 'login.html')
    if request.method == 'POST':
      nom = request.POST.get('fname', '')
      cognom = request.POST.get('lname', '')
      lloc = request.POST.get('lloc', '')
      edat = request.POST.get('edat', '')
      ip = func.get_client_ip(request)
      try:
        r = Registre(ip=ip)
        r.save()
      except:
        pass
      u = Usuari(nom=nom, cognom=cognom, edat=edat, resideix_a=lloc)
      u.save()
      # Send signal to fakeDNS.pid to make him update ip_table
      try:
        with open("/tmp/fakeDNS.pid","r") as pid_file:
          os.kill(int(pid_file.read()), signal.SIGUSR1)
      except Exception as e:
        print("Error enviant signal a fakeDNS: ", e)
      return redirect('/resources/')
    
def debug(request):
  return render(request,'login.html')

def home(request):
    if request.method == 'GET':
      return redirect('login')
    

@need_login
def resources(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def retrieve_frontend(request):
  if request.method == 'GET':
    return render(request,'statistics.html')


@basic_auth_required
def retrieve(request):
    if request.method == "GET":
      dia = datetime.datetime.now().day
      mes = datetime.datetime.now().month
      aany = 2019
      date = list([aany,mes,dia])
      if 'date' in request.GET:
        date = request.GET['date'].split('-')
      data = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
      file_path='/tmp/usuaris.csv'
      Usuari.objects.filter(registrat__gt = data).extra(
        select={
          'Prénom': 'nom',
          'Nom': 'cognom',
          'Email': 'email',
          'Âge': 'edat',
          'Lieu de naissance': 'nascut_a',
          'Lieu de résidence': 'resideix_a',
          'Date de connexion': 'registrat'

        }
      ).values(
        'Prénom', 'Nom', 'Email', 'Âge', 'Lieu de naissance', 'Lieu de résidence', 'Date de connexion'
      ).to_csv(file_path)
      with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/csv")
        response['Content-Disposition'] = 'inline; filename=usuaris.csv' 
        return response
      return HttpResponse(status=404)

@need_login
def wikipedia(request):
    if request.method == "GET":
      print('hkhk')

def view_404(request, exception=None):
  return redirect('login')
