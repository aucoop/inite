from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from portal import functions as func
from portal.models import Usuari, Registre
from inite.decorators import need_login



# Create your views here.

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

def retrieve(request):
    if request.method == "GET":
      file_path='/tmp/usuaris.csv'    
      Usuari.objects.to_csv(file_path)    
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
