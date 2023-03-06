from tabnanny import verbose
from django.db import models

class Servicio(models.Model):
    titulo = models.CharField(max_length=20)
    contenido = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='servicios')
    # Con auto_now_add=True le otorgara la fecha actual
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    # Clase interna para caracteristicas adicionales del modelo:
    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
    
    def __str__(self) -> str:
        return self.titulo