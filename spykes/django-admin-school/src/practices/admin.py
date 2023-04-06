from django.contrib import admin
from practices.models import PracticeArea, Practice, PracticeStudent


@admin.register(PracticeArea)
class PracticeAreaAdmin(admin.ModelAdmin):
    pass


class PracticeStudentInline(admin.StackedInline):
    model = PracticeStudent
    extra = 0


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    inlines = [PracticeStudentInline]
