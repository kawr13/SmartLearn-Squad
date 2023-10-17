from http.client import HTTPResponse

from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from Cabinet.models import Schedule, Cabinet
from profileapp.forms import UserForm, UserRegisterForm, CabinetForm, BlogForm, ServiceForm, CabinetTransferForm
from profileapp.models import Teacher, User, Tag, Post, EmailVerification, Service
# from Cabinet.models import Schedule
from django.contrib import auth
from django.shortcuts import render


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


def sort_category(request: HttpRequest, tag_id: int=None) -> render:
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
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        user_t = User.objects.get(id=user_id)
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
            return HttpResponseRedirect(reverse('profile:blog', args=(user_id,)))
    user = User.objects.select_related('teacher').get(id=user_id)
    teach = False
    form = BlogForm()
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
        'form': form,
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
        user = form.save()

        # Проверяем, установлена ли галочка "Преподаватель"
        is_teacher = form.cleaned_data.get('is_teacher')
        if is_teacher:
            # Создаем связанную запись Teacher и привязываем к пользователю
            teacher = Teacher.objects.create(description='', )  # Добавьте нужные атрибуты
            user.is_teacher = True
            user.teacher = teacher
            user.save()
            return HttpResponseRedirect(reverse('profile:login'))
        else:
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


def users_list(request: HTTPResponse) -> render:
    teach = Teacher.objects.get(id=request.user.id)
    print(teach)
    cab = Cabinet.objects.filter(teacher=teach).values('users')
    lst_user = []
    for i in cab:
        users = User.objects.get(id=i['users'])
        lst_user.append(users)
    print(lst_user)

    context = {
        'users': lst_user,
        'form': CabinetTransferForm(),
    }
    return render(request, 'profileapp/profile/users_list.html', context=context)
