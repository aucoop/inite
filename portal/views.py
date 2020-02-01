from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
import requests
from portal import functions as func
from portal.models import Usuari, Registre
from inite.decorators import need_login
import os
import signal
import datetime

# Create your views here.

def success(request):
  return HttpResponseNotFound('<h1>Page not found</h1>')
def login(request):
  if request.method == 'GET':
    ip = func.get_client_ip(request)
    try:
      r = Registre.objects.get(ip=ip)
      return redirect('/resources/')
    except:
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
      print("Ens disposem a enviar un signal...")
      with open("/tmp/fakeDNS.pid","r") as pid_file:
        print("Hem pogut obrir el fitcher del pid")
        os.kill(int(pid_file.read()), signal.SIGUSR1)
    except Exception as e:
      print("Error enviant signal a fakeDNS: ", e)
    return redirect('/resources/')

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('mostrarUnitats')
        return render(request, 'home.html')

@need_login
def resources(request):
    if request.method == 'GET':
        return render(request, 'index.html')

#@authorization
def retrieve(request):
    if request.method == "GET":
      dia = datetime.datetime.now().day
      mes = datetime.datetime.now().month
      aany = datetime.datetime.now().year
      if 'dia' in request.GET:
        dia = int(request.GET['dia'])
      if 'mes' in request.GET:
        mes = int(request.GET['mes'])
      if 'any' in request.GET:
        aany = int(request.GET['any'])
      data = datetime.datetime(aany,mes,dia)
      file_path='/tmp/usuaris.csv'
      qs = Usuari.objects.filter(registrat__gt=data)
      Usuari.objects.filter(registrat__gt = data).to_csv(file_path)
      data_dict = qs.values("nom","cognom", "email", "edat", "nascut_a", "resideix_a", "registrat") #retorna un diccionari
      print (data_dict)
      #Usuari.objects.to_csv(file_path)    
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
  return redirect('/login/')
