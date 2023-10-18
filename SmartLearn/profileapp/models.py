from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


class Requisites(models.Model):
    card_number = models.CharField(max_length=16)
    card_date = models.DateField()
    card_cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.card_number


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    is_teacher = models.BooleanField(default=False, blank=True, null=True)
    teacher = models.OneToOneField('Teacher', on_delete=models.CASCADE, related_name='user_teacher', null=True, blank=True)
    images = models.ImageField(upload_to='users/images', null=True, blank=True)
    requisites = models.OneToOneField('Requisites', on_delete=models.CASCADE, related_name='user_requisites', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


    def __str__(self):
        return self.username


class Teacher(models.Model):
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='teachers')

    def __str__(self):
        return f'{self.description} {self.pk}'


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     category_teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='category_teacher')
#
#     def __str__(self):
#         return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='service_teacher')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    images = models.ImageField(upload_to='posts/images', null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_category')
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


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification')
    created = models.DateTimeField(auto_now_add=True)
    expirations = models.DateTimeField()

    def __str__(self):
        return f'Email verification for {self.user} - {self.code} - {self.created}'

    # def send_verifications_email(self):
    #     link = reverse('accept', kwargs={'email': self.user.email, 'code': self.code})
    #     verifications_link = f'{settings.DOMAIN_NAME}{link}'
    #     subject = f'Подтверждение учетной записи для {self.user.username}'
    #     message = f'Для подтверждения учетной записи перейдите по ссылке: {verifications_link}'
    #     send_mail(
    #         subject=subject,
    #         message=message,
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[self.user.email],
    #         fail_silently=False
    #     )
    #
    # def is_expired(self):
    #     return True if now() >= self.expirations else False


class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='user_student', null=True, blank=True)

    # Другие поля студента

    def __str__(self):
        return f"Student {self.user.username}"



