from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator


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
            "Maximum 150 characters and minimum 1 character"
        ),
        validators=[MinLengthValidator(1)],
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        help_text=_(
            "Maximum 150 characters and minimum 1 character"
        ),
        validators=[MinLengthValidator(1)],
    )
    email = models.EmailField(
        _("email address"),
        max_length=254
    )
    nationality = models.ForeignKey(
        Nationality,
        on_delete=models.DO_NOTHING,
        verbose_name=_("nationality"),
        blank=False,
        null=True
    )
    start_date = models.DateField(
        verbose_name=_('start date'),
        null=True,
        blank=True
    )
    # Encrypted field
    dni = models.CharField(
        verbose_name=_('dni'),
        max_length=200,
    )

    def __str__(self):
        return self.username


class Employee(AppUser):
    vacation_days = models.IntegerField(
        _("vacation days"),
        default=0,
        help_text=_("Number of available vacation days"),
        blank=True
    )
    # Encrypted field
    bank_account = models.CharField(
        _("bank account"),
        max_length=200,
        validators=[
            MinLengthValidator(15),
            MaxLengthValidator(34),
        ],
        help_text=_("IBAN should have between 15 and 34 characters"),
        blank=True,
        null=True,
    )

    class Meta(AppUser.Meta):
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        # Greater to lower date
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return str(self.username)


class Student(AppUser):
    # Encrypted field
    passport = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_('passport'),
    )
    course_code = models.CharField(
        verbose_name=_('course code'),
        max_length=50,
        null=True,
        blank=True,
        help_text=_("Enrolled course code")
    )

    class Meta(AppUser.Meta):
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        # Greater to lower date
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return str(self.username)
