from django.shortcuts import render
from django.http import HttpResponse

def dash_admin(request):
    return HttpResponse("Bienvenue dans l'espace adminestrateur")


# Create your views here.
