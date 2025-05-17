from celery import shared_task
from django.core.mail import EmailMessage
from tools.pdf_generator import generate_pdf


@shared_task
def send_cv_pdf_email(template_path, context, recipient_email):
    pdf_file = generate_pdf(template_path, context)
    email = EmailMessage(
        subject="Your CV is ready",
        body="Please find your CV attached.",
        to=[recipient_email],
    )
    email.attach("cv.pdf", pdf_file, "application/pdf")
    email.send()
