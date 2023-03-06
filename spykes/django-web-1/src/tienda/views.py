from django.shortcuts import render
from tienda.models import Producto

def tienda(requests):
    productos = Producto.objects.all()
    return render(
        requests, 
        "tienda/tienda.html", 
        {"productos":productos}
    )