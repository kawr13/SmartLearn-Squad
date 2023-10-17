from http.client import HTTPResponse

from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from Cabinet.models import Schedule, Cabinet
from profileapp.forms import UserForm, UserRegisterForm, CabinetForm, BlogForm, ServiceForm, CabinetTransferForm
from profileapp.models import Teacher, User, Tag, Post, EmailVerification, Service, Students
# from Cabinet.models import Schedule
from django.contrib import auth
from django.shortcuts import render
from django.contrib import messages


def index(request: HttpRequest) -> render:
    if request.user.id:
        pers = User.objects.get(id=request.user.id).is_authenticated
    else:
        pers = False
    print(pers)
    context = {
        'title': 'Список учителей',
        'users': User.objects.select_related('teacher'),
        'regis': request.user,
        'autentic': pers,
        'categories': Tag.objects.all(),
    }
    return render(request, 'profileapp/profile/index.html', context=context)


def sort_category(request: HttpRequest, tag_id: int = None) -> render:
    if tag_id:
        context = {
            'users': User.objects.filter(teacher__tags__id=tag_id),
            'categories': Tag.objects.all(),
        }
    else:
        context = {
            'users': User.objects.select_related('teacher'),
            'categories': Tag.objects.all(),
        }

    return render(request, 'profileapp/profile/index.html', context=context)


def blog(request: HttpRequest, user_id: int) -> render:
    user = User.objects.select_related('teacher').get(id=user_id)
    teach = False
    if request.user.id:
        pers = User.objects.get(id=request.user.id).is_authenticated
    else:
        pers = False
    teacher = user.teacher
    if user.username == request.user.username:
        teach = True
    context = {
        'title': 'Блог',
        'user': user,
        'autentic': pers,
        'teach': teach,
        'posts': Post.objects.filter(teacher=teacher, is_private=False).order_by('-date_create'),
    }
    return render(request, 'profileapp/profile/blog.html', context=context)


def login(request: HttpRequest) -> render:
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = UserForm()
    context = {
        'title': 'Авторизация',
        'form': form,
    }
    return render(request, 'profileapp/profile/login.html', context=context)


class UserRegisterViews(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'profileapp/profile/register.html'
    success_url = reverse_lazy('profile:login')

    def form_valid(self, form):
        is_teacher = form.cleaned_data['is_teacher']
        user = form.save(commit=False)
        if is_teacher:
            user.is_teacher = True
        else:
            user.is_student = True
        user.save()
        if user.is_student:
            Students.objects.create(
                user=user,
            )
        elif user.is_teacher:
            teacher = Teacher.objects.create(description='', )
            user.teacher = teacher
        # Проверяем, установлена ли галочка "Преподаватель"

        return HttpResponseRedirect(reverse('profile:login'))

    def get_context_data(self, **kwargs):
        context = super(UserRegisterViews, self).get_context_data()
        return context


def profiluser(request: HttpRequest, user_id: int) -> render:
    if request.user.id:
        pers = User.objects.get(id=request.user.id).is_authenticated
    else:
        pers = False
    context = {
        'title': 'Профиль',
        'user': User.objects.get(id=user_id),
        'autentic': pers,
        'teacher': User.objects.select_related('teacher').get(id=user_id),
    }
    return render(request, 'profileapp/profile/profile.html', context=context)


def profilusercabinet(request: HttpRequest, user_id: int) -> render:
    if request.method == 'POST':
        form = CabinetForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile:profil_cabinet', kwargs={'user_id': user_id}))
    if request.user.id:
        pers = User.objects.get(id=request.user.id).is_authenticated
    else:
        pers = False
    teach = User.objects.get(id=user_id).teacher
    if teach:
        cabinets = Cabinet.objects.filter(teacher=teach)
    else:
        user = User.objects.get(id=user_id)
        teach = Cabinet.objects.filter(users=user)
        cabinets = Cabinet.objects.filter(users=user)

    users_by_cabinet = {}

    for cabinet in cabinets:
        users_by_cabinet[cabinet] = cabinet.users.filter(is_teacher=False)
    context = {
        'title': 'Кабинеты',
        'teach': teach,
        'autentic': pers,
        'users_by_cab': users_by_cabinet,
        'form': CabinetForm(),
    }
    return render(request, 'profileapp/profile/profile_cabinet.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


# def accepted_email(request, email, code):
#     user = User.objects.get(email=email)
#     email_verification = EmailVerification.objects.filter(user=user, code=code)
#     if email_verification.exists() and email_verification.first().is_expired():
#         user.is_verified_email = True
#         user.save()
#         return HttpResponseRedirect(reverse('profile:login'))
#     return render(request, 'profileapp/profile/accept.html')

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect(reverse('profile:blog', args=(request.user.id,)))


def services(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            servis = Service.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                teacher=User.objects.get(id=request.user.id).teacher,
            )
            servis.save()
            return HttpResponseRedirect(reverse('profile:services'))
    if request.user.id:
        pers = User.objects.get(id=request.user.id).is_authenticated
    form = ServiceForm()
    user_t = request.user.teacher
    service = Service.objects.filter(teacher=user_t)
    print(service)
    context = {
        'service': service,
        'autentic': pers,
        'form': form,
    }
    return render(request, 'profileapp/profile/services.html', context=context)


def edit_service(request, service_id):
    services = Service.objects.get(id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=services)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile:services'))
    else:
        form = ServiceForm(instance=services)
    context = {
        'form': form,
        'service_id': service_id,
    }

    return render(request, 'profileapp/profile/service_edit.html', context=context)


def users_list(request: HttpRequest) -> render:
    if request.method == 'POST':
        form = CabinetTransferForm(request.POST)
        if form.is_valid():
            target_cabinet = form.cleaned_data['target_cabinet']
            users_to_transfer = form.cleaned_data['users_to_transfer']
            # Для каждого пользователя, обновите их кабинет
            for user in users_to_transfer:
                # Удалите пользователя из текущего кабинета, если он уже принадлежит какому-либо кабинету
                if user.cabinets.exists():
                    current_cabinet = user.cabinets.first()
                    current_cabinet.users.remove(user)

                # Добавьте пользователя в выбранный кабинет
                target_cabinet.users.add(user)

            return redirect('profile:users_list')
    else:
        form = CabinetTransferForm()

    teach = Teacher.objects.get(id=request.user.id)
    cab = Students.objects.filter(teacher=teach)
    lst_user = []
    for i in cab:
        print(i)
        users = i.user
        lst_user.append(users)
        print(users.username)
    if request.user.id:
        pers = User.objects.get(id=request.user.id).is_authenticated
    context = {
        'users': lst_user,
        'form': form,
        'autentic': pers,
    }
    return render(request, 'profileapp/profile/users_list.html', context=context)


def publish_post(request):
    user_t = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                teacher=user_t.teacher,
                images=form.cleaned_data['images'],
                is_published=form.cleaned_data['is_published'],
                is_pinned=form.cleaned_data['is_pinned'],
                is_private=form.cleaned_data['is_private'],
            )
            post.save()
            return HttpResponseRedirect(reverse('profile:blog', args=(user_t.id,)))
    else:
        form = BlogForm()
    if request.user.id:
        pers = User.objects.get(id=request.user.id).is_authenticated
    else:
        pers = False
    if user_t.username == request.user.username:
        teach = True
    context = {
        'title': 'Блог',
        'user': user_t,
        'autentic': pers,
        'teach': teach,
        'form': form,
    }
    return render(request, 'profileapp/profile/post_poblich.html', context=context)
