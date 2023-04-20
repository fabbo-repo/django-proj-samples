from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    EMPLOYEE_DEFAULT_PERMISSIONS = [
        'view_appuser',
        'view_employee',
        'view_student',
        'view_agency',
        'view_practice',
        'add_practice',
        'change_practice',
        'delete_practice',
        'view_practicearea',
        'add_practicearea',
        'delete_practicearea',
        'view_vacation',
    ]

    def ready(self):
        import user.signals  # noqa
        try:
            from django.contrib.auth.models import Group, Permission
            default_employee_group, created = Group.objects.get_or_create(
                name='default_employee_group')
            default_employee_group.permissions.clear()
            
            # Default permissions for employee
            for permmission_code in self.EMPLOYEE_DEFAULT_PERMISSIONS:
                perm = Permission.objects.get(codename=permmission_code)
                default_employee_group.permissions.add(perm)
        except Exception: pass