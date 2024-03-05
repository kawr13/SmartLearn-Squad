from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

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
    is_online = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Teacher(models.Model):
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='teachers')
    max_peaple = models.IntegerField(blank=True, null=True)
    count_peaple = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.description} {self.pk}'


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})


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
    users = models.ManyToManyField(User, related_name='service_users')
    user_count = models.IntegerField()
    slug = models.SlugField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    content = models.TextField()
    images = models.ImageField(upload_to='posts/images', null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_category')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='post_teacher')
    is_published = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = (
            models.Index(fields=['is_published', 'is_pinned']),
            models.Index(fields=['-date_create']),
            models.Index(fields=['title','slug']),
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug,
                                       'year': self.date_create.year,'month': self.date_create.month,
                                       'day': self.date_create.day})

    def __str__(self):
        return self.title



class Comment(models.Model):
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')

    def __str__(self):
        return self.content


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification')
    created = models.DateTimeField(auto_now_add=True)
    expirations = models.DateTimeField()

    def __str__(self):
        return f'Email verification for {self.user} - {self.code} - {self.created}'


class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='user_student', null=True, blank=True)

    # Другие поля студента

    def __str__(self):
        return f"Student {self.user.username}"


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.total() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Baskets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='basket_service')
    quantity = models.PositiveIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Basket {self.service.name} for {self.user.username}"

    def total(self):
        return self.quantity * self.service.price



