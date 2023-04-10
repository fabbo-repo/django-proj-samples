from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        import user.signals  # noqa

        from django.contrib.auth.models import Group, Permission
        default_employee_group, created = Group.objects.get_or_create(
            name='default_employee_group')
        default_employee_group.permissions.clear()
        
        # Default permissions for employee
        view_appuser_perm = Permission.objects.get(codename='view_appuser')
        default_employee_group.permissions.add(view_appuser_perm)
        
        view_nationality_perm = Permission.objects.get(
            codename='view_nationality')
        default_employee_group.permissions.add(view_nationality_perm)
        
        view_employee_perm = Permission.objects.get(codename='view_employee')
        default_employee_group.permissions.add(view_employee_perm)
        
        view_student_perm = Permission.objects.get(codename='view_student')
        default_employee_group.permissions.add(view_student_perm)
        
        view_practice_perm = Permission.objects.get(codename='view_practice')
        default_employee_group.permissions.add(view_practice_perm)
        add_practice_perm = Permission.objects.get(codename='add_practice')
        default_employee_group.permissions.add(add_practice_perm)
        change_practice_perm = Permission.objects.get(codename='change_practice')
        default_employee_group.permissions.add(change_practice_perm)
        delete_practice_perm = Permission.objects.get(codename='delete_practice')
        default_employee_group.permissions.add(delete_practice_perm)
        
        view_practicearea_perm = Permission.objects.get(
            codename='view_practicearea')
        default_employee_group.permissions.add(view_practicearea_perm)
        add_practicearea_perm = Permission.objects.get(codename='add_practicearea')
        default_employee_group.permissions.add(add_practicearea_perm)
        change_practicearea_perm = Permission.objects.get(codename='change_practicearea')
        default_employee_group.permissions.add(change_practicearea_perm)
        delete_practicearea_perm = Permission.objects.get(codename='delete_practicearea')
        default_employee_group.permissions.add(delete_practicearea_perm)

        view_vacation_perm = Permission.objects.get(codename='view_vacation')
        default_employee_group.permissions.add(view_vacation_perm)
