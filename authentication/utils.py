from django.core.mail import EmailMessage

import os


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(to=data["to_email"],
            subject=data["email_subject"], body=data["email_body"])

        print(f"Mailing to {os.environ.get('EMAIL_HOST_USER')}")
        print(f"Password {os.environ.get('EMAIL_HOST_PASSWORD')}")

        email.send()
