from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path('', views.chat, name="chat"),
    path("<int:chat_id>/", views.room, name="room"),
    path('create_chat_d/<int:another_user_id>/', views.create_chat_dialog, name="create_chat"),
]
