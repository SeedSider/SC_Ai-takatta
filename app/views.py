from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import *
from .models import *
#import requests

# Create your views here.

def landing(request):
    html = 'landing.html'
    return render(request, html)

def soal(request):
    html = 'soal.html'
    return render(request, html)

def hasil(request):
    html = 'hasil.html'
    return render(request, html)