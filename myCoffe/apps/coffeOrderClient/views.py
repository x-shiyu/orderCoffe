from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    return HttpResponse('hello')
