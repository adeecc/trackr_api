from datetime import date
import requests
from celery import shared_task
from django.core.mail import EmailMessage


from .models import Document

@shared_task
def send_email(data):

    attachments = Document.objects.filter(todo_item=data["todo_item"])
    print(attachments)

    email = EmailMessage(to=data["to"],
            subject=data["subject"], body=data["body"])

    email.content_subtype = "html"

    # for attachment in data["attachments"]:
    #     url = 'https://shiftrio.blob.core.windows.net/media/' + (attachment.name)
    #     response = requests.get('https://shiftrio.blob.core.windows.net/media/' + (attachment.name))
    #     file_extension = attachment.name.split('.')[-1]
    #     email.attach(f'attachment.{file_extension}', response.content)

    print(f"{email.body}")
    email.send()
    print("Email Sent!!!")

    return None