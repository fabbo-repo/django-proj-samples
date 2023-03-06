from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    # Clase interna para caracteristicas adicionales del modelo:
    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
    
    def __str__(self) -> str:
        return self.nombre

class Post(models.Model):
    titulo = models.CharField(max_length=20)
    contenido = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='blog', null=True, blank=True)
    # Si se elimina un usuario se eliminarán todos los Post
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    # Clase interna para caracteristicas adicionales del modelo:
    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
    def __str__(self) -> str:
        return self.titulo