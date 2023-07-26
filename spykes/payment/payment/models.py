from django.db import models


class PaymentHistory(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField()

    def __str__(self):
        return self.date
