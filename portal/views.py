from django.shortcuts import render
import requests

# Create your views here.

def login(request):
  if request.method == 'GET':
	  return render(request, 'login.html')

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('mostrarUnitats')
        return render(request, 'home.html')

def resources(request):
    if request.method == 'GET':
        return render('index.html')

	
