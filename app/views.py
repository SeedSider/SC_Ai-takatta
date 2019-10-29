from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import *
from .models import *
#import requests

# Create your views here.

def index(request):
    html = 'landing.html'
    return render(request, html)
