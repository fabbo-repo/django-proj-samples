from django.db import models

class CategoriaProd(models.Model):
    nombre = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "categoria_prod"
        verbose_name_plural = "categorias_prod"

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(CategoriaProd, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="tienda", null=True, blank=True)
    precio = models.FloatField()
    disponibilidad = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.nombre
