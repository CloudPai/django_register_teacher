# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CreateUserView, MyObtainAuthToken
from .teacher_views import MyLoginView
from . import views
# urlpatterns = patterns('',
#                        url(r'^$', views.register, name='register'),
#                        url(r'^register/$', views.register, name='register'),
#                        )

urlpatterns = [
    # url(r'^$', views.register, name='register'),
    # url(r'^register/$', views.register, name='register'),
    url(r'^login/$', MyLoginView.as_view(), name='login'),#教师登录界面
    # #登录界面
    # url(r'^login/$', login, {'template_name': 'users/login.html'},
    #     name='login'),

]
