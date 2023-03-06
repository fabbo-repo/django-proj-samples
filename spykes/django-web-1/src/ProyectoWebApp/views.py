from django.shortcuts import render
from cesta_tienda.cesta_tienda import Cesta

def home(request):
    Cesta(request)
    return render(request, "ProyectoWebApp/home.html")