from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.safestring import mark_safe
from .models import *
# Register your models here.



class TagTabular(TabularInline):
    model = Teacher.tags.through
    list_display = ('name',)
    extra = 0


class StudentTabular(TabularInline):
    model = Students
    list_display = ('id',)
    extra = 0


@admin.register(Teacher)
class TeacherUsAdmin(admin.ModelAdmin):
    inlines = [TagTabular, StudentTabular]
    list_display = ('id', 'description',)
    fields = ('description',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Requisites)
class RequisitesAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'card_date', 'card_cvv')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name','phone_number', 'is_teacher', 'display_image')

    def display_image(self, obj):
        # Здесь вы можете создать HTML-код для отображения изображения
        if obj.images:
            return mark_safe(f'<img src="{obj.images.url}" width="50" height="50" />')
        else:
            return 'Нет изображения'

    display_image.short_description = 'Изображение'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category_teacher')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date_create', 'teacher', 'is_published', 'is_pinned', 'is_private')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'date_create', 'post', 'user')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('url', 'teacher', 'date_create')


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

# @admin.register(EmailVerification)
# class EmailVerificationAdmin(admin.ModelAdmin):
#     list_display = ('code', 'user', 'expirations')
#     fields = ('code', 'user', 'expirations', 'created')
#     readonly_fields = ('created',)

