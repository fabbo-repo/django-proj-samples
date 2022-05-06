from django.shortcuts import render, HttpResponse

def home(requests):
    return render(requests, "ProyectoWebApp/home.html")

def servicios(requests):
    return render(requests, "ProyectoWebApp/servicios.html")

def tienda(requests):
    return render(requests, "ProyectoWebApp/tienda.html")

def blog(requests):
    return render(requests, "ProyectoWebApp/blog.html")

def contacto(requests):
    return render(requests, "ProyectoWebApp/contacto.html")
