from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from utilits.my_multi import task, set_max_threads
from Project import settings
from .models import Complete
from ProfileApp.models import User
import time

set_max_threads(4)


@task
def send_mails(user_id=None, email=None, subject=None, message=None):
    try:
        send_mail(
            subject=subject,
            message=message,
            recipient_list=[email],
            from_email=settings.EMAIL_HOST_USER,
            fail_silently=False
        )
        successful = True
        time.sleep(2)
        if successful:
            user = User.objects.get(id=user_id)
            Complete.objects.create(user=user, message_complete=successful)
    except Exception as e:
        print(f"An error occurred during sending: {e}")
        
