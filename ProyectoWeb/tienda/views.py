from django.shortcuts import render

def tienda(requests):
    return render(requests, "tienda/tienda.html")