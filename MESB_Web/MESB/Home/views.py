from django.shortcuts import render

# Create your views here.

#Imports for Views
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the Home Screen!")