from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import Nationality


class Agency(models.Model):
    name = models.CharField(
        _('agency name'),
        primary_key=True,
        max_length=50
    )
    nationality = models.ForeignKey(
        Nationality, 
        on_delete=models.DO_NOTHING,
        verbose_name=_("nationality"),
        blank=False,
        null=True
    )
    email = models.EmailField(
        _("email address"),
        blank=True,
        max_length=254
    )
    web = models.URLField(
        _('web'),
        blank=True,
        max_length=200
    )
    commission = models.DecimalField(
        _('commission'),
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2
    )

    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)
