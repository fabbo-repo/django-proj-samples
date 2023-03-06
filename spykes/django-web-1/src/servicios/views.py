from django.shortcuts import render
from servicios.models import Servicio

def servicios(requests):
    servicios = Servicio.objects.all()
    return render(
        requests, 
        "servicios/servicios.html", 
        {"servicios":servicios}
    )