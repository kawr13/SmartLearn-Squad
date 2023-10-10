from django.contrib.auth.models import AbstractUser
from django.db import models


class Teacher(models.Model):
    description = models.TextField()
    tag = models.ManyToManyField('Tag', related_name='tag_teacher')

    def name_tag(self):
        return self.tag.name

    def __str__(self):
        return self.description


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    teacher = models.OneToOneField('Teacher', on_delete=models.CASCADE, related_name='user_teacher', null=True, blank=True)
    is_teacher = models.BooleanField(default=False)
    requisites = models.OneToOneField('Requisites', on_delete=models.CASCADE, related_name='user_requisites', null=True, blank=True)

    def __str__(self):
        return self.username


class Schedule(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date_create


class Cabinet(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cabinet_user')
    schedule = models.OneToOneField('Schedule', on_delete=models.CASCADE, related_name='cabinet_schedule')

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='service_teacher')

    def __str__(self):
        return self.name


class Requisites(models.Model):
    card_number = models.CharField(max_length=16)
    card_date = models.DateField()
    card_cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.card_number


class Category(models.Model):
    name = models.CharField(max_length=100)
    category_teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='category_teacher')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_category')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='post_teacher')
    is_published = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')

    def __str__(self):
        return self.content


class Record(models.Model):
    url = models.URLField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='record_teacher')
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



