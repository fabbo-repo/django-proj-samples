from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import Student


class PracticeArea(models.Model):
    name = models.CharField(
        verbose_name=_('practice area name'),
        primary_key=True,
        unique=True,
        max_length=40
    )

    class Meta:
        verbose_name = _('Practice Area')
        verbose_name_plural = _('Practice Areas')
        # Greater to lower date
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)


class Practice(models.Model):
    name = models.CharField(
        verbose_name=_('practice area name'),
        primary_key=True,
        unique=True,
        max_length=40
    )
    area = models.ForeignKey(
        PracticeArea,
        verbose_name=_('practice area'),
        on_delete=models.CASCADE
    )
    students = models.ManyToManyField(
        Student, 
        through='PracticeStudent',
        verbose_name=_('students'),
        blank=True
    )
    init_date = models.DateField(
        verbose_name=_('init date')
    )
    end_date = models.DateField(
        verbose_name=_('end date')
    )
    contact = models.CharField(
        verbose_name=_('contact number'),
        max_length=50,
        blank=True
    )
    address = models.TextField(
        verbose_name=_('address'),
        blank=True
    )
    email = models.EmailField( 
        verbose_name=_('mail'),
        max_length=254,
        blank=True
    )
    class Meta:
        verbose_name = _('Practice')
        verbose_name_plural = _('Practices')
        # Greater to lower date
        ordering = ['init_date']

    def __str__(self) -> str:
        return str(self.name)


class PracticeStudent(models.Model):
    practice = models.ForeignKey(
        Practice,
        verbose_name=_('practice'),
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        Student,
        verbose_name=_('student'),
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('practice', 'student')

    def __str__(self):
        return f"{self.practice.name} - {self.student.username}"
