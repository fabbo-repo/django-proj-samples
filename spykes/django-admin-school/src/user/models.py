from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from core.cryptography import encrypt_data
from django.core.validators import MinLengthValidator


class Nationality(models.Model):
    nationality = models.CharField(
        verbose_name=_('nationality'),
        primary_key=True,
        max_length=40
    )

    class Meta:
        verbose_name = _('Nationality')
        verbose_name_plural = _('Nationalities')
        # Greater to lower date
        ordering = ['nationality']

    def __str__(self) -> str:
        return str(self.nationality)


class AppUser(AbstractUser):
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        help_text=_(
            "Maximum 150 characters and minimum 1 character."
        ),
        validators=[MinLengthValidator(1)],
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        help_text=_(
            "Maximum 150 characters and minimum 1 character."
        ),
        validators=[MinLengthValidator(1)],
    )
    email = models.EmailField(_("email address"))
    nationality = models.ForeignKey(
        Nationality, on_delete=models.DO_NOTHING,
        verbose_name=_("nationality"),
        blank=False,
        null=True
    )


class Employee(AppUser):
    extra = models.CharField(
        verbose_name=_('extra'),
        max_length=40
    )

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        # Greater to lower date
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        self.is_staff = True
        self.is_superuser = False
        super(Employee, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.username)


class Student(AppUser):
    dni = models.CharField(
        verbose_name=_('dni'),
        max_length=200
    )

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        # Greater to lower date
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return str(self.username)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        self.is_staff = False
        self.is_superuser = False
        self.dni = encrypt_data(self.dni)
        super(Student, self).save(*args, **kwargs)
