from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('description', 'name_tag')


@admin.register(Requisites)
class RequisitesAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'card_date', 'card_cvv')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name','phone_number', 'teacher', 'is_teacher', 'requisites')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date_create',)


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'schedule')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_teacher')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date_create', 'category', 'teacher', 'is_published', 'is_pinned', 'is_private')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'date_create', 'post', 'user')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('url', 'teacher', 'date_create')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )