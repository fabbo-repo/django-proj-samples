from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Residence(models.Model):
    name = models.CharField(
        _('residence name'),
        primary_key=True,
        max_length=100
    )
    address = models.TextField(
        _('address'),
        blank=True,
        max_length=500
    )
    residence_owner = models.ForeignKey(
        ResidenceOwner,
        verbose_name=_('residence owner'),
        on_delete=models.CASCADE
    )
    residence_type = models.ForeignKey(
        ResidenceType,
        verbose_name=_('residence type'),
        on_delete=models.DO_NOTHING
    )
    start_date = models.DateTimeField(
        verbose_name=_('start date')
    )


    class Meta:
        verbose_name = _('Residence')
        verbose_name_plural = _('Residences')
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)


class ResidenceOwner(models.Model):
    name = models.CharField(
        _('residence owner name'),
        primary_key=True,
        max_length=150
    )
    contact = models.CharField( _('phone number'),blank=True, max_length=50)
    address = models.TextField(
        _('address'),
        blank=True,
        max_length=500
    )
    email = models.EmailField(blank=True, max_length=250)
    description = models.TextField(
        _('description'),
        blank=True,
        max_length=500
    )

    class Meta:
        verbose_name = _('Residence Owner')
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)

class ResidenceType(models.Model):
    SHARED_FLAT = 'SharedFlat'
    RESIDENCE = 'Residence'
    HOMESTAY = 'Homestay'
    RESIDENCE_CHOICES = [
        (SHARED_FLAT, 'Shared Flat'),
        (RESIDENCE, 'Residence'),
        (HOMESTAY, 'Homestay')
    ]
    type = models.CharField(max_length=20, choices=RESIDENCE_CHOICES)

    class Meta:
        verbose_name = 'Residence Type'
        verbose_name_plural = 'Residence Types'

    def __str__(self):
        return self.type
