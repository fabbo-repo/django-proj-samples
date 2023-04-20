from django.contrib import admin
from agencies.models import Agency

# Register your models here.
@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
    )
    search_fields=(
        'name',
        'email',
        'web',
    )
