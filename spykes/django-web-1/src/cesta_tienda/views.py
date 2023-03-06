from django.shortcuts import render, redirect
from cesta_tienda.cesta_tienda import Cesta
from tienda.models import Producto

def agregar_producto(request, prod_id):
    cesta = Cesta(request)
    prod = Producto.objects.get(id=prod_id)
    cesta.agregar(producto=prod)
    return redirect("Tienda")

def eliminar_producto(request, prod_id):
    cesta = Cesta(request)
    prod = Producto.objects.get(id=prod_id)
    cesta.eliminar(producto=prod)
    return redirect("Tienda")
    
def restar_producto(request, prod_id):
    cesta = Cesta(request)
    prod = Producto.objects.get(id=prod_id)
    cesta.restar_producto(producto=prod)
    return redirect("Tienda")
    
def limpiar_cesta(request):
    cesta = Cesta(request)
    cesta.limpiar_cesta()
    return redirect("Tienda")