from django.shortcuts import render, HttpResponse
from servicios.models import Servicio

def home(requests):
    return render(requests, "ProyectoWebApp/home.html")

def servicios(requests):
    servicios = Servicio.objects.all()
    return render(
        requests, 
        "ProyectoWebApp/servicios.html", 
        {"servicios":servicios}
    )

def tienda(requests):
    return render(requests, "ProyectoWebApp/tienda.html")

def blog(requests):
    return render(requests, "ProyectoWebApp/blog.html")

def contacto(requests):
    return render(requests, "ProyectoWebApp/contacto.html")
