from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

globalCounter = 0

def index(request):
    return HttpResponse("Hello, world. You're at the ubike/vis index.")

def counter(request):
    return HttpResponse("The cron.yaml has already call this function for " + str(globalCounter) + " times since 7/24 16:30")

def count(request):
    global globalCounter
    globalCounter += 1
    return HttpResponse("added")