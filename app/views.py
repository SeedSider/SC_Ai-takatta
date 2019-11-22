from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt

def landing(request):
    html = 'landing.html'
    # decide()
    return render(request, html)

def soal(request):
    html = 'soal.html'
    return render(request, html)

@csrf_exempt
def hasil(request):
    # bikin logic nya disini aja
    html = 'hasil.html'
    print (request.POST)
    
    return render(request, html)