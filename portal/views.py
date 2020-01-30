from django.shortcuts import render
import requests
from portal import functions as func
from portal.models import Usuari
# Create your views here.

def login(request):
  if request.method == 'GET':
	  return render(request, 'login.html')
  if request.method == 'POST':
    nom = request.POST.get('fname', '')
    cognom = request.POST.get('lname', '')
    lloc = request.POST.get('lloc', '')
    edat = request.POST.get('edat', '')
    ip = func.get_client_ip(request)
    print(nom, cognom, lloc, edat, ip)
    u = Usuari(nom=nom, cognom=cognom, edat=edat, resideix_a=lloc)
    u.save()
    return render(request, 'index.html')

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('mostrarUnitats')
        return render(request, 'home.html')

def resources(request):
    if request.method == 'GET':
        return render(request, 'index.html')

	
