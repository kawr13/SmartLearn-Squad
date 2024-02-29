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
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import sort_category, blog, logining, UserRegisterViews, logout, profilusercabinet, delete_post, \
    edit_service, users_list, publish_post, delete_service, sevices_pay, \
    ProfileUserView, DeleteView, ProfileServices, ServiceOrderView, PaysView, DeleteBasket, PostDetailed

app_name = 'profile'

urlpatterns = [
    path('tag/<int:tag_id>/', sort_category, name='tag'),
    path('blog/<int:user_id>/', blog, name='blog'),
    path('post_detailed/<int:post_id>/', PostDetailed.as_view(), name='post_detailed'),
    path('login/', logining, name='login'),
    path('register/', UserRegisterViews.as_view(), name='register'),

    path('logout/', logout, name='logout'),
    path('profils/<int:user_id>/', ProfileUserView.as_view(), name='updateViews'),
    path('profils/cabinet/<int:user_id>/', profilusercabinet, name='profile_cabinet'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('services/', ProfileServices.as_view(), name='services'),
    path('edit_serv/<int:service_id>/', edit_service, name='edit_service'),
    path('delete_service/<int:service_id>/', delete_service, name='delete_serv'),
    path('users/', users_list, name='users_list'),
    path('publish/', publish_post, name='publish_post'),
    path('pay_service/<int:service_id>/', sevices_pay, name='pay_service'),
    path('pays/', PaysView.as_view(), name='pays'),
    path('services_pay/', ServiceOrderView.as_view(), name='services_pay'),
    path('delete_bask/<int:basket_id>/', DeleteBasket.as_view(), name='delete_bask'),
    path('delete_cab/<int:cabinet_id>/', DeleteView.as_view(), name='delete_cab'),
]
