from django.shortcuts import render


def index(request):
    return render(request, "ChatApp/index.html")


def room(request, room_name):
    return render(request, "ChatApp/room.html", {"room_name": room_name})