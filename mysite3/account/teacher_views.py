# coding=utf-8
from __future__ import unicode_literals
from __future__ import division
import collections
import json

from io import StringIO
# from StringIO import StringIO


from django.contrib.auth.views import LoginView
from .forms import MyAuthenticationForm
from django.core import serializers
from django.contrib import messages
from django.forms import model_to_dict

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
from django_tables2 import RequestConfig

# from .tables import ProdcutionTable, ProdcutionDownloadTable
# from .models import Class, Teacher, School, User,#Production, TeacherScore, ANTLRScore, ProductionHint
# from .forms import MyAuthenticationForm
# from gen.Gen import gen

class MyLoginView(LoginView):
    authentication_form = MyAuthenticationForm
    LOGIN_REDIRECT_URL = '/index'
    redirect_authenticated_user = False
    extra_context = {'class': "form-control"}

