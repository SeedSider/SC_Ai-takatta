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

def qanda(request):

    # MASIH ANEH

    # print(request.POST[''])
    print(request.POST['1'])
    # response_data = {}
    # for k, v in request.POST.items():
    #     question = k
    #     answer = v

    #     response_data[k] = question
    #     response_data[v] = answer

    # print(response_data)

    # response_data = {"a" : "s"}
    # return JsonResponse(response_data)

    # return render(request, 'soal.html')
    return HttpResponse("success")

