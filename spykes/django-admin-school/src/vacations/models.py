from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import Employee


class Vacation(models.Model):
    employee = models.ForeignKey(
        Employee,
        verbose_name=_('employee'),
        on_delete=models.CASCADE
    )
    init_date = models.DateField(
        verbose_name=_('init date')
    )
    end_date = models.DateField(
        verbose_name=_('end date')
    )

    class Meta:
        verbose_name = _('Vacation')
        verbose_name_plural = _('Vacations')
        # Greater to lower date
        ordering = ['init_date']

    def __str__(self) -> str:
        return " - ".join(
            [
                self.init_date.strftime("%d/%m/%Y"),
                self.end_date.strftime("%d/%m/%Y")
            ]
        )
