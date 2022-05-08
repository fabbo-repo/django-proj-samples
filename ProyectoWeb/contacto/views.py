from django.shortcuts import render
from contacto.forms import FormularioContacto

def contacto(requests):
    formulario = FormularioContacto()
    return render(
        requests, 
        "contacto/contacto.html",
        {"formulario":formulario}
    )
