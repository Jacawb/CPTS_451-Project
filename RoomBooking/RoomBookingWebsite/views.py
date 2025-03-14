from django.shortcuts import render, HTTPResponse

# Create your views here.

def home(request):
    return HTTPResponse("Welcome")
