# -*- coding: utf-8 -*-

from rest_framework import serializers, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from .models import User, Production, School, Class
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    student_class = serializers.StringRelatedField(read_only=True, source='Student', allow_null=True, allow_empty=True)
    student_class_second = serializers.StringRelatedField(read_only=True, source='Student', allow_null=True, allow_empty=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError(detail={'code': '1', 'message': u'重复的用户名'}, code=status.HTTP_409_CONFLICT)
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError(detail={'code':'2', 'message':u'密码长度过短'}, code=status.HTTP_400_BAD_REQUEST)
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            name=validated_data['name'],
            sex=validated_data['sex'],
            age=validated_data['age'],
            grade=validated_data['grade'],
            student_id=validated_data['student_id'],
            school=validated_data['school'],
            school_second=validated_data['school_second'],
            student_class=validated_data['student_class'],
            student_class_second=validated_data['student_class_second']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        write_only_fields = ['password']
        fields = ['username', 'password', 'name', 'sex', 'age', 'grade', 'student_id',
                  'school', 'student_class', 'school_second', 'student_class_second']
        extra_kwargs = {
            'school': {'allow_null': True, 'allow_empty': True},
            'school_second': {'allow_null': True, 'allow_empty': True},
        }


class MyAuthTokenSerializer(AuthTokenSerializer):
    """
    custom Serializer that check request auth info
    """

    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    raise serializers.ValidationError(
                       detail={'username': {'message': u'用户未启用', 'code': '1'}},
                       code='authorization')
            else:
                raise serializers.ValidationError(
                    detail={'username': {'message': u'用户名或密码不正确', 'code': '2'}},
                    code='authorization')
        else:
            raise serializers.ValidationError(
                detail={'username': {'message': u'必须有用户名或密码', 'code': '3'}},
                code='authorization')

        attrs['user'] = user
        return attrs


class ProductionCreateSerializer(serializers.ModelSerializer):

    file = serializers.FileField()
    image = serializers.ImageField()
    # author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        if Production.objects.filter(author__exact=attrs['author'], name__exact=attrs['name']).exists():
            raise serializers.ValidationError(
                detail={'name': {'message': u'该用户已经拥有相同名称的文件', 'code': '1'}})
        return attrs


    class Meta:
        model = Production
        fields = ['author', 'name', 'file', 'update_time', 'create_time', 'image']
        read_only_fields = ()


class ProductionUpdateSerializer(serializers.ModelSerializer):

    file = serializers.FileField()
    image = serializers.ImageField()

    class Meta:
        model = Production
        fields = ['file', 'image']


class ProductionDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Production
        fields = ['id']
        read_only_fields = ('id', )


class ProductionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Production
        fields = ['id', 'file', 'update_time', 'name', 'image']
        read_only_fields = ('id', 'file', 'update_time')


class SchoolSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if School.objects.filter(school_name__exact=attrs['school_name']).exists():
            raise serializers.ValidationError(
                detail={'name': {'message': u'学校已经存在', 'code': '1'}})
        return attrs

    class Meta:
        model = School
        fields = ['school_name']


class ClassListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ('class_name', )


class ClassCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if Class.objects.filter(school_name__exact=attrs['school_name'], class_name=attrs['class_name']).exists():
            raise serializers.ValidationError(
                detail={'name': {'message': u'学校班级已经存在', 'code': '1'}})
        return attrs

    class Meta:
        model = Class
        fields = ['school_name', 'class_name']
