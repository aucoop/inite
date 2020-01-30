from django.shortcuts import render
import requests
import functions 

# Create your views here.

def login(request):
  if request.method == 'GET':
	  return render(request, 'login.html')
  if request.method == 'POST':
    nom = request.POST.get('fname', '')
    cognom = request.POST.get('lname', '')
    lloc = request.POST.get('lloc', '')
    edat = request.POST.get('edat', '')
    
    return render(request, 'index.html')

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('mostrarUnitats')
        return render(request, 'home.html')

def resources(request):
    if request.method == 'GET':
        return render(request, 'index.html')

	
