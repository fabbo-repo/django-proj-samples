from django.contrib import admin
from residences.models import Residence,ResidenceOwner

# Register your models here.
@admin.register(Residence)
class ResidenceAdmin(admin.ModelAdmin):
    search_fields=('name')

@admin.register(ResidenceOwner)
class ResidenceOwnerAdmin(admin.ModelAdmin):
    search_fields=('name')