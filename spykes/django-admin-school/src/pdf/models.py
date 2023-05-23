from django.db import models

class PdfCertificate(models.Model):
    pdf1 = models.FileField(upload_to='pdf1')
    pdf2 = models.FileField(upload_to='pdf2')