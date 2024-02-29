from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from utilits.my_multi import task, set_max_threads
from utilits.DecoratorTheard import threaClass
from Project import settings

set_max_threads(4)


@threaClass
def send_mails(email=None, subject=None, message=None):
    try:
        send_mail(
            subject=subject,
            message=message,
            recipient_list=[email],
            from_email=settings.EMAIL_HOST_USER,
            fail_silently=False
        )
        successful = True
    except Exception as e:
        successful = False
        print(f"An error occurred during sending: {e}")
    return successful