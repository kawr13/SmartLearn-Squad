from django.contrib import admin
from django.contrib.admin import TabularInline
from .models import *



@admin.register(Schedule)
class ScheduleViewAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ScheduleAdmin(TabularInline):
    model = Schedule
    extra = 0


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'teacher', 'users')
    inlines = [ScheduleAdmin]
