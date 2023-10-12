from django.contrib.auth.models import AbstractUser
from django.db import models


class Requisites(models.Model):
    card_number = models.CharField(max_length=16)
    card_date = models.DateField()
    card_cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.card_number


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    is_teacher = models.BooleanField(default=False)
    teacher = models.OneToOneField('Teacher', on_delete=models.CASCADE, related_name='user_teacher', null=True, blank=True)
    images = models.ImageField(upload_to='users/images', null=True, blank=True)
    requisites = models.OneToOneField('Requisites', on_delete=models.CASCADE, related_name='user_requisites', null=True, blank=True)


class Schedule(models.Model):
    date_create = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.date_create)


class Teacher(models.Model):
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='teachers')

    def __str__(self):
        return self.description


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cabinet(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher, related_name='cabinets')
    users = models.ManyToManyField(User, related_name='cabinets')
    schedules = models.ManyToManyField(Schedule, related_name='cabinets')

    def __str__(self):
        return self.name



# class CabinetUser(models.Model):
#     user = models.ManyToManyField(User, related_name='cabinet_user')
#     cabinet = models.OneToOneField('Cabinet', on_delete=models.CASCADE, related_name='user_cabinet')
#     date_create = models.DateTimeField(auto_now_add=True)
#
#
# class CabinetTeacher(models.Model):
#     teacher = models.ManyToManyField(Teacher, related_name='cabinet_teacher')
#     cabinet = models.OneToOneField('Cabinet', on_delete=models.CASCADE, related_name='teacher_cabinet')
#     date_create = models.DateTimeField(auto_now_add=True)


# class ServiceTeacher(models.Model):
#     teacher = models.ManyToManyField(Teacher, related_name='service_teacher')
#     cabinet = models.OneToOneField('Cabinet', on_delete=models.CASCADE, related_name='service_cabinet')
#     date_create = models.DateTimeField(auto_now_add=True)



class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='service_teacher')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    category_teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='category_teacher')

    def __str__(self):
        return self.name

# class CategoryTeacher(models.Model):
#     teacher = models.ManyToManyField(Teacher, related_name='category_teacher')
#     category = models.ManyToManyField(Category, related_name='category')


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

