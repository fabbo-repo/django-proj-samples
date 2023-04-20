from django.contrib import admin
from practices.admin import PracticeStudentInline
from user.models import Student, Employee, Nationality, AppUser
from vacations.admin import VacationsInline
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

admin.site.register(Nationality)


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'nationality',
        'is_active',
        'is_staff',
        'is_superuser',
        'user_permissions',
        'groups',
    )
    filter_horizontal = (
        'user_permissions',
        'groups',
    )

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'dni',
        'nationality',
    ]
    readonly_fields = [
        'date_joined',
        'last_login',
    ]
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
            self.readonly_fields.append("username")
            fieldsets += ((
                _('Authentication'),
                {'fields': ('date_joined', 'last_login',)}),)
        if request.user and not request.user is AnonymousUser \
                and request.user.is_superuser:
            permission_fields = (
                'is_active',
                'is_staff',
                'is_superuser',
                'user_permissions',
            )
            fieldsets += ((
                _('Permissions'),
                {'fields': permission_fields}),)
            self.filter_horizontal += ('user_permissions',)
        return fieldsets


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'first_name',
        'last_name',
        'nationality',
        'dni',
        'passport',
        'course_code',
    )
    readonly_fields = (
        'date_joined',
        'last_login',
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
