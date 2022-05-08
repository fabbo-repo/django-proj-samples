from django.contrib import admin
from tienda.models import Producto, CategoriaProd

class CategoriaProdAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(CategoriaProd, CategoriaProdAdmin)
admin.site.register(Producto, ProductoAdmin)