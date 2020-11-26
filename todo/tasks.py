from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_email(data):
    email = EmailMessage(to=data["to"],
            subject=data["subject"], body=data["body"])

    print(f"{email.body}")
    email.send()
    print("Email Sent!!!")
    return None