from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def pagina_vacia(request):
    return HttpResponse("Esta es una página vacía.")
