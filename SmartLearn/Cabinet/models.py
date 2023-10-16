from django.db import models

from profileapp.models import Teacher, User
from django.utils.timezone import now

# Create your models here.



class Cabinet(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher, related_name='cabinets')
    users = models.ManyToManyField(User, related_name='cabinets')

    def __str__(self):
        return self.name


class Schedule(models.Model):
    cabinet = models.ForeignKey('Cabinet', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.URLField()
    date_create = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    an_dellet = models.BooleanField(default=False)

    def time_end(self):
        if now() > self.date_end:
            pass

