"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import sort_category, blog, logining, UserRegisterViews, logout, profiluser, profilusercabinet, delete_post, \
    services, edit_service, users_list, publish_post

app_name = 'profile'

urlpatterns = [
    path('tag/<int:tag_id>/', sort_category, name='tag'),
    path('blog/<int:user_id>/', blog, name='blog'),
    path('login/', logining, name='login'),
    path('register/', UserRegisterViews.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('profils/<int:user_id>/', profiluser, name='updateViews'),
    path('profils/cabinet/<int:user_id>/', profilusercabinet, name='profile_cabinet'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('services/', services, name='services'),
    path('edit_serv/<int:service_id>/', edit_service, name='edit_service'),
    path('users/', users_list, name='users_list'),
    path('publish/', publish_post, name='publish_post'),
]
