# encoding=utf-8
from __future__ import unicode_literals
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _


class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': "用户名"}),
        label=_("用户名"),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "密码"}, ),
    )
