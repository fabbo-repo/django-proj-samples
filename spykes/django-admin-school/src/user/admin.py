from django.contrib import admin
from practices.admin import PracticeStudentInline
from user.models import Student, Employee, Nationality
from vacations.admin import VacationsInline
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

# Remove Groups from admin
admin.site.unregister(Group)

admin.site.register(Nationality)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'nationality',
        'extra',
    )
    readonly_fields = (
        'date_joined',
        'last_login'
    )
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_filter = (
        'nationality',
    )
    search_fields = (
        'username', 
        'email',
        'first_name',
        'last_name',
    )
    inlines = (
        VacationsInline,
    )

    def get_fieldsets(self, request, obj=None):
        """
        Remove the password field from the displayed fields
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        if not obj:
            fieldsets += ((_('Password'), {'fields': ('password',)}),)
        else:
            fieldsets += ((
                _('Authentication'),
                {'fields': ('date_joined', 'last_login',)}),)
        return fieldsets


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'nationality',
        'dni',
    )
    readonly_fields = (
        'date_joined',
        'last_login'
    )
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_filter = (
        'nationality',
    )
    search_fields = (
        'username', 
        'email',
        'first_name',
        'last_name',
        'dni',
    )
    inlines = [PracticeStudentInline]

    def get_fieldsets(self, request, obj=None):
        """
        Remove the password field from the displayed fields
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        if obj:
            fieldsets += ((
                _('Authentication'),
                {'fields': ('date_joined', 'last_login',)}),)
        return fieldsets
