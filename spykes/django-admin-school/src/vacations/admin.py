from django.contrib import admin
from vacations.models import Vacation


class VacationsInline(admin.StackedInline):
    model = Vacation
    extra = 0


@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    pass
