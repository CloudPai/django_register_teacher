# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User, Teacher ,School, Class#Production, ANTLRScore, ProductionHint, TeacherScore,

from .models import User
# from .tasks import run

# Register your models here.

#  ----------------------START OF CUSTOM TEACHER ADMIN-----------------------------------------------

class TeacherCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ('username', 'email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(TeacherCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class TeacherChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Teacher
        fields = ('username', 'email', 'name')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class TeacherAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = TeacherChangeForm
    add_form = TeacherCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'name', 'email')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'name')
    ordering = ('username',)
    filter_horizontal = ()


#  ----------------------END OF CUSTOM TEACHER ADMIN-----------------------------------------------



# admin.site.register(Student, UserAdmin)
# admin.site.register(Teacher, TeacherAdmin)
# admin.site.register(Production, ProductionAdmin)
# admin.site.register(ANTLRScore, ANTLRScoreAdmin)
# admin.site.register(ProductionHint, ProductionHintAdmin)
# admin.site.register(TeacherScore)
admin.site.register(School)
admin.site.register(Class)
admin.site.register(User)