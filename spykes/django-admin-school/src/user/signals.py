from django.db.models.signals import post_init, pre_save, post_save
from django.dispatch import receiver
from core.cryptography import decrypt_data, encrypt_data
from user.models import Student, Employee, AppUser
from django.contrib.auth.models import Group


@receiver(post_init, sender=AppUser)
def decrypt_appuser_dni(sender, instance, **kwargs):
    if instance.dni:
        instance.dni = decrypt_data(instance.dni)

@receiver(post_init, sender=Employee)
def decrypt_employee_bank_account(sender, instance, **kwargs):
    if instance.bank_account:
        instance.bank_account = decrypt_data(instance.bank_account)

@receiver(post_init, sender=Student)
def decrypt_student_passport(sender, instance, **kwargs):
    if instance.passport:
        instance.passport = decrypt_data(instance.passport)

@receiver(pre_save, sender=Employee)
def pre_save_employee(sender, instance, **kwargs):
    if not instance.pk:
        print("hola")
        instance.is_staff = True
        instance.is_superuser = False
        instance.bank_account = encrypt_data(instance.bank_account)


@receiver(post_save, sender=Employee)
def post_save_employee(sender, instance, created, **kwargs):
    user = AppUser.objects.get(username=instance.username)
    default_employee_group = Group.objects.get(
        name='default_employee_group')
    user.groups.add(default_employee_group)


@receiver(pre_save, sender=AppUser)
def pre_save_appuser(sender, instance, **kwargs):
    instance.is_staff = False
    instance.is_superuser = False
    instance.dni = encrypt_data(instance.dni)

@receiver(pre_save, sender=Student)
def pre_save_student(sender, instance, **kwargs):
    instance.passport = encrypt_data(instance.passport)