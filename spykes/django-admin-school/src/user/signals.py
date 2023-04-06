from django.db.models.signals import post_init
from django.dispatch import receiver
from core.cryptography import decrypt_data
from user.models import Student


@receiver(post_init, sender=Student)
def decrypt_student_dni(sender, instance, **kwargs):
    if instance.dni:
        instance.dni = decrypt_data(instance.dni)
