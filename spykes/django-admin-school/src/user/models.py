from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):

class Student(AbstractUser):
    subject = models.FloatField(
        verbose_name = _("expected monthly balance"),
        validators = [MinValueValidator(0.0)],
        default = 0.0
    )