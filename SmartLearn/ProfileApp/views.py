from http.client import HTTPResponse
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from CabinetApp.models import Schedule, Cabinet
from ProfileApp.forms import UserForm, UserRegisterForm, CabinetForm, BlogForm, ServiceForm, CabinetTransferForm, UserProfileForm
from ProfileApp.models import Teacher, User, Tag, Post, EmailVerification, Service, Students, Baskets
# from Cabinet.models import Schedule
from django.contrib import auth
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Prefetch, Count
from django.db import transaction
from django.core.cache import cache
from icecream import ic


class IndexView(View):

    def get(self, request: HttpRequest) -> render:
        if request.user.is_authenticated:
            bas_quant = Baskets.objects.filter(user=request.user).total_quantity()
        else:
            bas_quant = 0

        context = {
            'title': 'Список учителей',
            'users': User.objects.prefetch_related('teacher'),
            'regis': request.user,
            'autentic': request.user.is_authenticated,
            'categories': Tag.objects.all(),
            'bas_quant': bas_quant,
        }
        return render(request, 'profileapp/profile/index_start.html', context=context)


def sort_category(request: HttpRequest, tag_id: int = None) -> render:
    if request.user.is_authenticated:
        bas_quant = Baskets.objects.filter(user=request.user).total_quantity()
    else:
        bas_quant = 0
    categories = Tag.objects.all()
    if tag_id:
        users = ic(User.objects.filter(teacher__tags__id=tag_id).prefetch_related('teacher'))
    else:
        users = User.objects.select_related('teacher').prefetch_related('teacher')
    context = {
        'users': users,
        'categories': categories,
        'title': 'Список учителей',
        'regis': request.user,
        'autentic': request.user.is_authenticated,
        'bas_quant': bas_quant,
    }
    return render(request, 'profileapp/profile/index_start.html', context=context)


def blog(request: HttpRequest, user_id: int) -> render:
    user = User.objects.get(id=user_id)
    teach = False
    teacher = user.teacher
    if request.user.is_authenticated:
        bas_quant = Baskets.objects.filter(user=request.user).total_quantity()
    else:
        bas_quant = 0
    if user == request.user:
        teach = True
    context = {
        'title': 'Блог',
        'user_auth': user,
        'autentic': request.user.is_authenticated,
        'teach': teach,
        'posts': Post.objects.filter(teacher=teacher, is_private=False).order_by('-date_create'),
        'prices': Service.objects.filter(teacher=teacher),
        'bas_quant': bas_quant,
    }
    return render(request, 'profileapp/profile/new_blog_page.html', context=context)


def logining(request):
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Неверный логин или пароль')
        else:
            messages.error(request, 'Неверный логин или пароль')
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
            teacher = Teacher.objects.create(description='')
            ic(teacher)
            user.teacher = teacher
            ic(user.teacher)
            teacher.user_teacher = ic(user)
            ic(teacher.user_teacher)
        else:
            user.is_student = True
        user.save()
        if user.is_student:
            with transaction.atomic():
                Students.objects.create(user=user)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(UserRegisterViews, self).get_context_data(**kwargs)
        return context


class ProfileUserView(View):
    def get(self, request: HttpRequest, user_id: int) -> render:
        form = UserProfileForm(instance=request.user)
        status = None
        if request.user.id:
            pers = User.objects.get(id=request.user.id).is_authenticated
            user = User.objects.get(id=user_id)
            if user.is_teacher:
                status = 'teacher'
            else:
                status = 'student'
        else:
            pers = False

        context = {
            'title': 'Профиль',
            'user': User.objects.get(id=user_id),
            'autentic': pers,
            'teacher': User.objects.select_related('teacher').get(id=user_id),
            'status': status,
            'form': form,
        }
        print(status)
        return render(request, 'profileapp/profile/profile.html', context=context)

    def post(self, request: HttpRequest, user_id: int) -> render:
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile:updateViews', kwargs={'user_id': user_id}))
        else:
            return HttpResponseRedirect(reverse('profile:updateViews', kwargs={'user_id': user_id}))


def profilusercabinet(request: HttpRequest, user_id: int) -> render:
    if request.method == 'POST':
        teacher = Teacher.objects.get(user_teacher=user_id)
        form = CabinetForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            student = form.cleaned_data['users']
            cabinet = Cabinet.objects.create(name=name, teacher=teacher)
            cabinet.users.set(student)
            return HttpResponseRedirect(reverse('profile:profile_cabinet', kwargs={'user_id': user_id}))

    if request.user.id:
        pers = User.objects.get(id=request.user.id).is_authenticated
    else:
        pers = False
    user = User.objects.get(id=user_id)
    teacher = None
    cabinets = None

    if user.is_teacher:
        teacher = user.teacher
        ic(teacher)
        cabinets = Cabinet.objects.filter(teacher=teacher)
    else:
        # Пользователь - студент, найдите связанных преподавателей и кабинеты
        student = Students.objects.get(user=user)
        teacher = student.teacher
        cabinets = Cabinet.objects.filter(users=user)

    users_by_cabinet = {}
    for cabinet in cabinets:
        users = list(cabinet.users.all())
        users.sort(key=lambda user: (user.is_teacher, user.username))
        users_by_cabinet[cabinet] = users

    print(users_by_cabinet)
    context = {
        'title': 'Кабинеты',
        'teach': teacher,
        'autentic': pers,
        'users_by_cab': users_by_cabinet,
        'form': CabinetForm(),
    }
    return render(request, 'profileapp/profile/profile_cabinet.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def delete_post(request, post_id):
    Post.objects.filter(id=post_id).delete()
    return HttpResponseRedirect(reverse_lazy('profile:blog', args=(request.user.id,)))


class ProfileServices(View):
    def get(self, request):
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

    def post(self, request: HttpRequest) -> render:
        form = ServiceForm(request.POST)
        if form.is_valid():
            servis = Service.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                user_count=form.cleaned_data['user_count'],
                price=form.cleaned_data['price'],
                teacher=User.objects.get(id=request.user.id).teacher,
            )
            servis.save()
            if Tag.objects.filter(name=form.cleaned_data['name']).exists():
                tag = Tag.objects.get(name=form.cleaned_data['name'])
                tag.teachers.add(User.objects.get(id=request.user.id).teacher)
            else:
                tag = Tag.objects.create(name=form.cleaned_data['name'])
                tag.teachers.add(User.objects.get(id=request.user.id).teacher)
            return HttpResponseRedirect(reverse('profile:services'))


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


def delete_service(request, service_id):
    services = Service.objects.get(id=service_id)
    tag = Tag.objects.get(name=services.name)
    if tag.teachers.exists():
        tag.teachers.remove(User.objects.get(id=request.user.id).teacher)
    services.delete()
    return HttpResponseRedirect(reverse_lazy('profile:services'))


class DeleteView(View):
    def post(self, request, cabinet_id):
        cabinet = Cabinet.objects.get(id=cabinet_id)
        if cabinet.users.count() > 0:
            return HttpResponseRedirect(reverse_lazy('profile:profile_cabinet', kwargs={'user_id': request.user.id}))
        cabinet.delete()

        return  HttpResponseRedirect(reverse_lazy('profile:profile_cabinet', kwargs={'user_id': request.user.id}))


def users_list(request: HttpRequest) -> render:
    teacher = request.user.teacher

    if request.method == 'POST':
        form = CabinetTransferForm(request.POST)
        if request.POST.get('users_to_transfer') is not None:
            if form.is_valid():
                ic('trulala')
                target_cabinet = form.cleaned_data['target_cabinet']
                users_to_transfer = form.cleaned_data['users_to_transfer']
                delete_cabinet = request.POST.get('delete_cabinet')
                ic(request.POST)

                with transaction.atomic():
                    if delete_cabinet:
                        user_to_delete = User.objects.get(id=delete_cabinet)
                        user_to_delete.cabinets.clear()

                    for user in users_to_transfer:
                        # Проверьте, принадлежит ли пользователь кабинету другого учителя
                        if user.cabinets.exists():
                            current_cabinet = user.cabinets.first()
                            if current_cabinet.teacher != teacher:
                                # Если пользователь принадлежит другому учителю, не удаляйте его
                                pass
                            else:
                                # Удалите пользователя из текущего кабинета, если он уже принадлежит какому-либо кабинету
                                current_cabinet.users.remove(user)

                        # Добавьте пользователя в выбранный кабинет
                        target_cabinet.users.add(user)

            return redirect('profile:users_list')
        else:
            messages.error(request, 'Пожалуйста, проверьте введенные данные. Некоторые поля заполнены неверно.')
            return redirect('profile:users_list')
    else:
        # Обновите queryset для target_cabinet и target_users, чтобы они возвращали только кабинеты и пользователей текущего учителя
        form = CabinetTransferForm()

        target_cabinets = Cabinet.objects.filter(teacher=teacher).select_related('teacher')
        target_users = User.objects.filter(cabinets__in=target_cabinets)
        cache_key = f"students_list:{teacher.pk}"
        lst_user = cache.get(cache_key)

        if lst_user is None:
            with transaction.atomic():
                students = Students.objects.filter(teacher=teacher)
                lst_user = target_users
                ic(students)
                cache.set(cache_key, lst_user, 300)

        form.fields['target_cabinet'].queryset = target_cabinets
        form.fields['users_to_transfer'].queryset = target_users



    pers = request.user.is_authenticated

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


# def profile_info_teacher(request: HttpRequest, teacher_id: int) -> render:
#     teacher = Teacher.objects.get(id=teacher_id)
#     posts = Post.objects.filter(teacher=teacher)
#     context = {
#         'user': teacher,
#         'posts': posts,
#     }
#     return render(request, 'profileapp/profile/profile_info_teacher.html', context=context)


def sevices_pay(request, service_id):
    service = Service.objects.get(id=service_id)
    basket = Baskets.objects.filter(user=request.user, service=service)
    if not basket.exists():
        Baskets.objects.create(user=request.user, service=service, quantity=1)
    else:
        basket = basket.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostDetailed(View):
    def get(request: HttpRequest, post_id: int) -> render:
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
        return render(request, 'profileapp/profile/blog.html', context=context)


class ServiceOrderView(View):
    def get(self, request):
        if request.user.is_authenticated:
            baskets = Baskets.objects.filter(user=request.user)
            context = {
                'title': 'Оформление',
                'user_id': request.user.id,
                'baskets': baskets,
                'autentic': request.user.is_authenticated,
            }
        else:
            context = {
                'title': 'Оформление',
                'autentic': False,
            }
        return render(request, 'profileapp/profile/services_pays.html', context=context)


class PaysView(View):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        baskets = Baskets.objects.filter(user=user)
        for basket in baskets:
            teach = Teacher.objects.get(id=basket.service.teacher.id)
            cabinet_query = Cabinet.objects.filter(name='Общий кабинет', teacher=teach)
            if not cabinet_query.exists():
                cabinet = Cabinet.objects.create(name='Общий кабинет', teacher=teach)
                cabinet.save()
            else:
                cabinet = cabinet_query.first()
            cabinet.users.add(user)
            cabinet.save()
            basket.delete()
        return HttpResponse('Оплата прошла успешно')


class DeleteBasket(View):
    def get(self, request, basket_id):
        basket = Baskets.objects.get(id=basket_id)
        if basket.quantity > 1:
            basket.quantity -= 1
            basket.save()
        else:
            basket.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


