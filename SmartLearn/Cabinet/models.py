from django.db import models

from profileapp.models import Teacher, User
from django.utils.timezone import now

# Create your models here.


class Cabinet(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='cabinets', null=True, blank=True)
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
        return now() > self.date_end if self.date_end else False

