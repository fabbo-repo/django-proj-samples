from django.urls import path
from autenticacion.views import VistaRegistro, cerrar_cesion, loguear

urlpatterns = [
    path('', VistaRegistro.as_view(), name="Autenticacion"),
    path('cerrar_sesion', cerrar_cesion, name="CerrarSesion"),
    path('login', loguear, name="Login")
]