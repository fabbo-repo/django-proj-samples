from django.urls import path
from . import views

# El app_name se añade delante del atributo name de las urls
# para evitar colisiones
app_name="cesta"

urlpatterns = [
    path('agregar/<int:prod_id>/', views.agregar_producto, name="agregar"),
    path('eliminar/<int:prod_id>/', views.eliminar_producto, name="eliminar"),
    path('restar/<int:prod_id>/', views.restar_producto, name="restar"),
    path('limpiar/', views.limpiar_cesta, name="limpiar")
]