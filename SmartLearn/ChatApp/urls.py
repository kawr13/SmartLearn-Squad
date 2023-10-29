from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path('', views.chat, name="chat"),
    # path("", views.index, name="index"),
    path("<int:chat_id>/", views.room, name="room"),
    path('create_chat/<int:teacher_id>/', views.create_chat, name="create_chat"),
]