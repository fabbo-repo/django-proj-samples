from django.contrib import admin
from user.models import Student, Employee, Nationality
from django.contrib.auth.models import Group

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
        'date_joined',
        'last_login',
        'nationality',
        'extra',
    )
    readonly_fields = (
        'date_joined',
        'last_login'
    )
    list_display = (
        'username',
    )

    def get_fieldsets(self, request, obj=None):
        """
        Remove the password field from the displayed fields
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        if not obj:
            fieldsets += (('Password', {'fields': ('password',)}),)
        else:
            print(obj)
        return fieldsets


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'date_joined',
        'last_login',
        'nationality',
        'dni',
    )
    readonly_fields = (
        'date_joined',
        'last_login'
    )
    list_display = (
        'username',
    )

    def get_fieldsets(self, request, obj=None):
        """
        Remove the password field from the displayed fields
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        if obj: obj.dni = obj.get_dni()
        return fieldsets