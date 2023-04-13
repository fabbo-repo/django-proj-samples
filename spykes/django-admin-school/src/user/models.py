from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.contrib.auth.models import Group
from django.utils import timezone

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


class AppUserManager(UserManager):
    pass

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

    start_date = models.DateField(
        verbose_name=_('start date'),
        default=timezone.now,
    )

    dni = models.CharField(
        primary_key=True,
        max_length=20,
        help_text=_(
            "Introduce your document id"
        )
    )
    
    objects = AppUserManager()

    def __str__(self):
        return self.username


class Employee(AppUser):
    #vacation = models.ForeignKey(
    #    Vacation,
    #    on_delete=models.DO_NOTHING,
    #    verbose_name=_("vacation"),
    #    null=True,
    #    blank=True,
    #)

    vacation_days = models.IntegerField(
        _("vacation days"),
        default=0,
        help_text=_("Number of vacation days available"),
        blank=True
    )

    bank_account = models.CharField(
        _("bank account"),
        max_length=34,
        validators=[
            MinLengthValidator(15),
            MaxLengthValidator(34),
        ],
        help_text=_("The IBAN should have between 15 and 34 characters."),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        # Greater to lower date
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super(Employee, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.username)


class Student(AppUser):

    passport = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_('passport'),
        help_text= _("Passport document")
    )

    course_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('course code'),
        help_text=_("Code of the course enrolled")
    )

    #residence = models.ForeignKey(
    #    Residence,
    #    on_delete=models.DO_NOTHING,
    #    null=True,
    #    blank=True,
    #    verbose_name=_('residence')
    #)

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        # Greater to lower date
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return str(self.username)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super(Student, self).save(*args, **kwargs)
