from django.contrib import admin
from pdf.models import PdfCertificate


@admin.register(PdfCertificate)
class PdfCertificateAdmin(admin.ModelAdmin):
    readonly_fields = [
        "pdf1",
        "pdf2"
    ]
