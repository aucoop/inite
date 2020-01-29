from django.shortcuts import render
import requests

# Create your views here.

def login(request):
  if request.method == 'GET':
	  return render(request, 'login.html')

	
