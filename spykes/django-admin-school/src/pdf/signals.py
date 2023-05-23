from django.db.models.signals import post_init, pre_save, post_save
from django.dispatch import receiver
from core.cryptography import decrypt_data, encrypt_data
from user.models import Student, Employee, AppUser
from reportlab.pdfgen import canvas
import io
from pdf.models import PdfCertificate
from django.core.files.base import ContentFile


@receiver(pre_save, sender=PdfCertificate)
def pre_save_employee(sender, instance, **kwargs):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(0, 0, "Hello world.")
    p.showPage()
    p.save()
    buffer.seek(0)
    content = ContentFile(buffer.getvalue())
    buffer.close()
    instance.pdf1.save('certificate.pdf', content, save=False)