from celery import shared_task
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .models import Report
import time
import os
from django.conf import settings

os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
@shared_task
def generate_pdf_report(report_id):

    report = Report.objects.get(id=report_id)
    report.status = "processing"
    report.save()

    time.sleep(5)

    file_path = os.path.join(settings.MEDIA_ROOT, f"report_{report.id}.pdf")

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = [
        Paragraph(f"Report: {report.title}", styles["Title"]),
        Paragraph(f"ID: {report.id}", styles["Normal"]),
    ]

    doc.build(content)

    report.file.name = f"report_{report.id}.pdf"
    report.status = "done"
    report.save()

    return "done"