from .models import Student
import time
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
def run_this_function():
    print("Function Started")
    print("Function Started..")

    time.sleep(2)

    print("Function Executed")


def send_email_to_client():
    try:
        subject = "This mail is from Django Server"
        message = (
            "This is a test message from Django Server Email  hosted by Dilesh Bisen"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [os.getenv('EMAIL')]

        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        pass

def send_email_with_attachment(subject, message, recipient_list, file_path):
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )
    mail.attach_file(file_path)
    mail.send()
