from django.contrib import messages
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

from CabinetApp.forms import RecordsForms, SendEmailForm
from CabinetApp.models import Cabinet, Schedule, Record
from ProfileApp.models import User, Post
from utilits.utilites_tools import SendMessages


# Create your views her
def get_events(request, cabinet_id):
    cabinet = Cabinet.objects.get(id=cabinet_id)
    now = timezone.now()
    Schedule.objects.filter(cabinet=cabinet, date_end__lt=now).delete()

    events = Schedule.objects.filter(cabinet=cabinet).values('date_create', 'date_end', 'url', 'title')
    event_data = []
    for event in events:
        event_data.append({
            'title': event['title'],
            'urls': event['url'],
            'start': event['date_create'].isoformat(),
            'end': event['date_end'].isoformat() if event['date_end'] else None,
        })
    return JsonResponse(event_data, safe=False)


# def calendar_view(request: HttpRequest) -> render:
#     return render(request, 'CabinetApp/calend.html')


def cabinets_view(request: HttpRequest, cab_id: int) -> render:
    if request.user.id:
        pers = User.objects.get(id=request.user.id).is_authenticated
    else:
        pers = False
    print(pers)
    context = {
        'title': 'Кабинеты',
        'cabinet_id': cab_id,
        'autentic': pers,
    }
    return render(request, 'Cabinet/cabinet.html', context=context)


def update_calend(request: HttpRequest, cabinet_id) -> render:
    if request.method == 'POST':
        date_string = request.POST
        print(date_string)
        if date_string:
            cabinet = Cabinet.objects.get(pk=cabinet_id)
            schedule = Schedule.objects.create(
                cabinet=cabinet,
                title=date_string['title'],
                url=date_string['urls'],
                date_create=date_string['start'],
                date_end=date_string['end'],
            )
            print(schedule)
            schedule.save()

            return redirect('cabinet:cabinet', cab_id=cabinet_id)


def user_full(request: HttpRequest, cabinet_id) -> render:
    if request.user.id:
        pers = User.objects.get(id=request.user.id)
    else:
        pers = False
    teachs = Cabinet.objects.get(pk=cabinet_id).teacher
    post = Post.objects.filter(teacher=teachs, is_private=True).order_by('-date_create')
    context = {
        'title': 'Полезная информация',
        'autentic': pers.is_authenticated,
        'teach': teachs,
        'user_id': pers.id,
        'posts': post,
        'cabinet_id': cabinet_id,
    }
    return render(request, 'Cabinet/userfull_info_cab.html', context=context)


class VideoArchView(View):

    def get(self, request, cabinet_id):
        form = RecordsForms()
        if request.user.id:
            pers = User.objects.get(id=request.user.id)
        else:
            pers = False
        cabinet = Cabinet.objects.get(pk=cabinet_id)
        teachs = cabinet.teacher
        records = Record.objects.filter(cabinet=cabinet)
        context = {
            'title': 'Архив записей видео',
            'autentic': pers.is_authenticated,
            'teach': teachs,
            'user_id': pers.id,
            'records': records,
            'cabinet_id': cabinet_id,
            'form': form,
        }
        return render(request, 'Cabinet/records.html', context=context)

    def post(self, request, cabinet_id):
        form = RecordsForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            url = form.cleaned_data['url']
            cabinet = Cabinet.objects.get(pk=cabinet_id)
            record = Record.objects.create(title=title, url=url, cabinet=cabinet, teacher=cabinet.teacher)
            record.save()
            return redirect('cabinet:records_cab', cabinet_id=cabinet_id)


def user_full_view(request: HttpRequest, post_id: int) -> render:
    if request.user.id:
        pers = User.objects.get(id=request.user.id)
    else:
        pers = False
    post = Post.objects.get(id=post_id)
    context = {
        'title': 'Полезная информация',
        'user_id': pers.id,
        'autentic': pers.is_authenticated,
        'posts': post,
    }
    return render(request, 'Cabinet/userfull_detailed.html', context=context)


class SendToEmailView(View):

    def get(self, request, cabinet_id):
        if request.user.id:
            pers = User.objects.get(id=request.user.id)
        else:
            pers = False
        cabinet = Cabinet.objects.get(pk=cabinet_id)
        teachs = cabinet.teacher
        users = Cabinet.objects.get(pk=cabinet_id).users.filter(is_student=True)
        # form = SendEmailForm(initial={'user': users})
        form = SendEmailForm()
        form.fields['user'].queryset = users
        context = {
            'title': 'Архив записей видео',
            'autentic': pers.is_authenticated,
            'teach': teachs,
            'user_id': pers.id,
            'cabinet_id': cabinet_id,
            'form': form,
        }
        return render(request, 'Cabinet/cabinet_send_email.html', context=context)

    def post(self, request, cabinet_id):
        form = SendEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            users = form.cleaned_data['user']
            msg = form.cleaned_data['message']
            is_lesson = form.cleaned_data['is_lesson']
            cabinet = Cabinet.objects.get(pk=cabinet_id)
            if is_lesson:
                records_exist = Record.objects.filter(cabinet=cabinet, teacher=cabinet.teacher).last()
                if records_exist:
                    msg += '\n' + records_exist.url
            for user in users:
                with SendMessages(email=user.email, subject=subject, message=msg) as send:
                    if send.successful:
                        messages.success(request, 'Сообщение отправлено')
                        return HttpResponseRedirect(reverse('сabinet:send_mail', args=[cabinet_id]))
                    else:
                        messages.error(request, 'Сообщение не отправлено')
                        return HttpResponseRedirect(reverse('сabinet:send_mail', args=[cabinet_id]))
