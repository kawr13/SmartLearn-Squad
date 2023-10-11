from django.db import models


# Create your models here.
class Cabinet(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher, related_name='cabinets')
    users = models.ManyToManyField(User, related_name='cabinets')
    schedules = models.ManyToManyField(Schedule, related_name='cabinets')

    def __str__(self):
        return self.name


class Schedule(models.Model):
    date_create = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.date_create)