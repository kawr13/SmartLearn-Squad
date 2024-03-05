from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Complete
from django.contrib.sessions.models import Session

@receiver(post_save, sender=Complete)
def notify_on_complete(sender, instance, created, **kwargs):
    print('notify_on_complete')
