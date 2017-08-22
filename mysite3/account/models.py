# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, UserManager)

import uuid

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, UserManager
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, UserManager)
import os

# from .storage import OverwriteStorage

# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     email = models.EmailField()
#     school = models.CharField(max_length=50)
#     realName = models.CharField(max_length=50)
#
#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email','school','realName','password',)

# admin.site.register(User, UserAdmin)

# 以下内容导入自902scratch_api
# 以下内容导入自902scratch_api
# 以下内容导入自902scratch_api

class MyUserManager(BaseUserManager):
#manager定义了create_user()和create_superuser()方法
    """
    The default User Model is too crowd, we use Custom BaseUserManager instead
    """

    def create_user(self, username, password=None):
        """
        create a user
        :param username: username of new User
        :param password: password of new User
        :return: A BaseUser object
        """

        user = self.model(
            username=username,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        create a superuser, this is use for "python manage createsuperuser"
        :param username: name of new superuser
        :param password: password of new superuser
        :return: a BaseUser object with is_admin set to True
        """

        user = self.create_user(username, password)
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser):#BaseUser 为重写的django的用户模型
    username = models.CharField(max_length=30, unique=True, primary_key=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ()

    class Meta:
        ordering = ('-username',)#按用户名降序排列，-表示降序

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):#user是否拥有app中访问models的权限
        return True

    @property  #通过@property装饰器在model中预定义方法实现 , 如使用 user.is_staff 判断是否允许user访问admin界面
    def is_staff(self):
        return self.is_admin

# 此处名称原来为User，为了防止与原来的冲突，更改为Student
class User(BaseUser):
    """
    用户/学生模型
    """

    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    grade = models.CharField(max_length=30, null=True)
    student_id = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey('School', max_length=50, null=True, blank=True, related_name='user_school')
    student_class = models.ForeignKey('Class', max_length=30, null=True, blank=True, related_name='user_class')
    school_second = models.ForeignKey('School', max_length=50, null=True, blank=True, related_name='user_school_2')
    student_class_second = models.ForeignKey('Class', max_length=30, null=True, blank=True,
                                             related_name='user_class_2')



    class Meta:
        ordering = ('-username',)

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):#has_perm(perm)：判断用户是否具有特定权限,
                                        # checks whether the user has a specific permission
        return True

    def has_module_perms(self, app_label):#checks whether the user has any permissions for that app
        return True

    @property ##通过@property装饰器在model中预定义方法实现 如使用 user.is_admin 查询是否允许user访问admin界面
    def is_staff(self):
        return self.is_admin



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    create a auth token for every User 
    """
    if created:
        Token.objects.create(user=instance)


def get_upload_path(instance, filename):
    """
    set upload path for Production.file
    """
    # print (os.path.join(instance.author.username, filename))
    return os.path.join(instance.author.username, instance.name+'.sb2')


def get_image_path(instance, filename):
    """
    set upload path for Production.image
    """
    return os.path.join(instance.author.username, instance.name + '_' + filename)


class Teacher(BaseUser):
    """
    教师模型 
    """
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)


    class Meta:
        ordering = ('-username',)#按用户名降序排列，-表示降序



    def __unicode__(self):#
        return self.name

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


# class Production(models.Model):
#     """
#     作品模型
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=50, verbose_name='作品名称')
#     author = models.ForeignKey(User, null=True, verbose_name='作者')
#     file = models.FileField(upload_to=get_upload_path, storage=OverwriteStorage(), verbose_name='下载地址')
#     is_active = models.BooleanField(default=True)
#     # fix bugs of create_time and update_time
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#     update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
#     image = models.ImageField(null=True, upload_to=get_image_path, storage=OverwriteStorage())
#
#     def __unicode__(self):
#         return self.author.name + '的' + self.name
#
#     def __str__(self):
#         return self.author.name + '的' + self.name
#
#     def get_full_name(self):
#         return self.name
#
#     def get_short_name(self):
#         return self.name
#
#
# class ANTLRScore(models.Model):
#     """
#     ANTLR生成得分模型
#     """
#     production_id = models.OneToOneField(Production, to_field='id')
#     ap_score = models.IntegerField()
#     parallelism_score = models.IntegerField()
#     synchronization_score = models.IntegerField()
#     flow_control_score = models.IntegerField()
#     user_interactivity_score = models.IntegerField()
#     logical_thinking_score = models.IntegerField()
#     data_representation_score = models.IntegerField()
#
#
# class ProductionHint(models.Model):
#     """
#     作品提示模型
#     """
#     production_id = models.ForeignKey(Production, to_field='id')
#     hint = models.CharField(max_length=100)
#
#
# class TeacherScore(models.Model):
#     """
#     教师评分模型
#     """
#     production_id = models.OneToOneField(Production, to_field='id')
#     score = models.IntegerField()
#     comment = models.TextField(null=True, max_length=2000)
#
#
class School(models.Model):
    """
    学校模型
    """
    school_name = models.CharField(primary_key=True, max_length=50)

    def __unicode__(self):
        return self.school_name

    def __str__(self):
        return self.school_name


class Class(models.Model):
    """
    班级模型
    """
    id = models.AutoField(primary_key=True)
    school_name = models.ForeignKey(School, to_field='school_name')
    class_name = models.CharField(max_length=40)
    teacher = models.ManyToManyField(Teacher, blank=True)

    class Meta:
        unique_together = (("school_name", "class_name"),)


#__str_和__unicode__的作用是美化打印出来的结果，使人类更方便查看
    #如果是Python2的话就使用__unicode__方法
    def __unicode__(self):
        return self.class_name

    # 如果用的是Python3的话就只能用__str__方法
    def __str__(self):
        return self.class_name




