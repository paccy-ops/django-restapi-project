import threading
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['subject'], body=data['body'], to=[data['to_email']])
        EmailThread(email).start()
        # email.send(fail_silently=False)

    @staticmethod
    def after_verification(data):
        email = EmailMessage(subject=data['subject'], body=data['body'], to=[data['to_email']])
        EmailThread(email).start()

    @staticmethod
    def send_email_account_status(data, html_content):
        mail = EmailMultiAlternatives(subject=data['subject'], body=data['body'], from_email=settings.EMAIL_HOST_USER, to=[data['to_email']])
        mail.attach_alternative(html_content, "text/html")
        EmailThread(mail).start()
