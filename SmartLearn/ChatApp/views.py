from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, Chat, User
from icecream import ic
from django.db.models import Q


@login_required
def index(request):
    return render(request, "ChatApp/index.html")


@login_required()
def room(request, chat_id):
    chat_list = Chat.objects.filter(members=request.user)
    messages = Message.objects.filter(chat=chat_id).order_by('-timestamp')
    return render(request, "ChatApp/room.html", {
        "chat_id": chat_id,
        'user': request.user.username,
        'messages': messages,
        'chat_list': chat_list,

    })


@login_required()
def chat(request):
    chat_list = Chat.objects.filter(members=request.user)
    context = {
        'user': request.user,
        'chat_list': chat_list,
    }

    return render(request, "ChatApp/chat.html", context=context)


# @login_required()
# def search_view(request):
#     search_query = request.GET.get('search_query')
#     results = User.objects.filter(name__icontains=search_query) if search_query else User.objects.all()
#
#     return render(request, 'ChatApp/chat.html', {'results': results})


def create_chat(request, teacher_id):
    teacher = User.objects.get(id=teacher_id)
    user = request.user
    chat = Chat.objects.filter(members=teacher).filter(members=user).first()
    if not chat:
        new_chat = Chat.objects.create(type=Chat.DIALOG)
        new_chat.members.add(teacher, user)
        return redirect('chat:room', new_chat.id)

    return redirect('chat:room', chat.id)
