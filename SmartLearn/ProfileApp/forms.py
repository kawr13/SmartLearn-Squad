from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from CabinetApp.models import Cabinet
from ProfileApp.models import User, EmailVerification, Service, Students
from tinymce.widgets import TinyMCE


class UserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Логин или пароль неверны.')
        return cleaned_data


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_teacher = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Преподаватель'), (False, 'Студент')]),
        label="Роль"
    )
    images = forms.ImageField(label='Изображение', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number',
                  'is_teacher', 'images', 'is_student']



class CabinetForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    users = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_teacher=False), required=False)

    class Meta:
        model = Cabinet
        fields = ['name', 'users']


# class DeleteCabinetForm(forms.Form):
#     un_delete = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check'}), required=False)

class BlogForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    images = forms.ImageField(label='Изображение', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    is_published = forms.BooleanField(label='Опубликовано', widget=forms.CheckboxInput(attrs={'class': 'form-check'}),
                                    required=False)
    is_pinned = forms.BooleanField(label='Закреплено', widget=forms.CheckboxInput(attrs={'class': 'form-check'}),
                                    required=False)
    is_private = forms.BooleanField(label='Приватно', widget=forms.CheckboxInput(attrs={'class': 'form-check'}),
                                    required=False)

    class Meta:
        model = User
        fields = ['title', 'content', 'images', 'is_published', 'is_pinned', 'is_private']


class ServiceForm(UserChangeForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='Цена', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    user_count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Service
        fields = ('name', 'description', 'price', 'user_count')


class CabinetTransferForm(forms.Form):
    target_cabinet = forms.ModelChoiceField(queryset=Cabinet.objects.all(), empty_label="Выберите кабинет")
    users_to_transfer = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    images = forms.ImageField(label='Изображение', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'images')
