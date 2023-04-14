from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Agency(models.Model):
    name = models.CharField(
        _('agency name'),
        primary_key=True,
        max_length=50
    )
    nationality = models.CharField(
        _('nationality'),
        blank=True,
        max_length=50
    )
    web = models.URLField(blank=True, max_length=200)

    email = models.EmailField(blank=True, max_length=250)

    commission = models.DecimalField(blank=True, max_digits=5, decimal_places=2)


    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)
