from django.core.mail import send_mail

from Project import settings


class SendMessages:
    def __init__(self, email, subject, message):
        self.email = email
        self.subject = subject
        self.message = message
        self.successful = False

    def __enter__(self):
        self.send()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None or exc_val is not None:
            print(f"An error occurred during sending: {exc_val}")
            self.successful = False
        else:
            pass

    def send(self):
        try:
            send_mail(
                subject=self.subject,
                message=self.message,
                recipient_list=[self.email],
                from_email=settings.EMAIL_HOST_USER,
                fail_silently=False
            )
            self.successful = True
        except Exception as e:
            print(f"An error occurred during sending: {e}")
