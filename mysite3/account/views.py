#coding=utf-8
from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from .models import User
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions, status
from .serializers import UserSerializer


#定义表单模型
# class UserForm(forms.Form):
#     username = forms.CharField(label='用户名：',max_length=100)
#     passworld = forms.CharField(label='密码：',widget=forms.PasswordInput())
#     email = forms.EmailField(label='电子邮件：')
#     school = forms.CharField(label='学校：',max_length=100)
#     realName = forms.CharField(label='真实姓名：',max_length=100)
#
# # Create your views here.
# def register(request):
#     if request.method == "POST":
#         uf = UserForm(request.POST)
#         if uf.is_valid():
#             #获取表单信息
#             username = uf.cleaned_data['username']
#             passworld = uf.cleaned_data['passworld']
#             email = uf.cleaned_data['email']
#             school = uf.cleaned_data['school']
#             realName = uf.cleaned_data['realName']
#             #将表单写入数据库
#             user = User()
#             user.username = username
#             user.passworld = passworld
#             user.email = email
#             user.school = school
#             user.realName = realName
#             user.save()
#             #返回注册成功页面
#             return render_to_response('success.html',{'username':username})
#     else:
#         uf = UserForm()
#     return render_to_response('register.html',{'uf':uf})



# 以下内容导入自902scratch_api
# 以下内容导入自902scratch_api
# 以下内容导入自902scratch_api



class CreateUserView(CreateAPIView):
    """
    Create a new User
    """
    model = User
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data.copy()
        class_object1= Class.objects.filter(school_name=request.data['school'],
                                            class_name=request.data['student_class'])
        if class_object1:
            class_object1 = class_object1[0]
        else:
            class_object1 = None
            data['student_class'] = ""
            # return Response(data={'code': '3', 'message': '找不到班级!'}, status=status.HTTP_201_CREATED)

        class_object2 = Class.objects.filter(school_name=request.data['school_second'],
                                             class_name=request.data['student_class_second'])
        if class_object2:
            class_object2 = class_object2[0]
        else:
            class_object2 = None
            data['student_class_second'] = ""
            # return Response(data={'code': '3', 'message': '找不到班级!'}, status=status.HTTP_201_CREATED)
        print(data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(student_class=class_object1, student_class_second=class_object2)
            return Response(data={'code': '0', 'message': 'Success!'}, status=status.HTTP_201_CREATED)
        else:
            return Response("Error!", status=status.HTTP_400_BAD_REQUEST)


class MyObtainAuthToken(ObtainAuthToken):
    """
    Login Auth
    In order to return specific code, we rewrite TokenSerializer class
    """
    serializer_class = MyAuthTokenSerializer





def scratch(request):
    return render_to_response("scratch.html");



def analysis(request):
    if request.method == "GET":
        r = add.delay(3, 4)
        print(r.get())
        c = {}
        c.update(csrf(request))
        return render_to_response("upload_file.html", c)


class SchoolView(ListAPIView):
    """
    创建一个学校或者获取学校列表
    """
    model = School
    permission_classes = (permissions.AllowAny, )
    serializer_class = SchoolSerializer
    queryset = School.objects.all()

    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={'code': '0', 'message': 'Success!'}, status=status.HTTP_201_CREATED)
        else:
            return Response("Error!", status=status.HTTP_400_BAD_REQUEST)


class ClassListView(ListAPIView):
    """
    获取一个学校的班级列表
    """
    model = Class
    permission_classes = (permissions.AllowAny, )
    serializer_class = ClassListSerializer

    def get_queryset(self):
        schoolname = self.request.data['school_name']
        print(schoolname)
        return Class.objects.filter(school_name=schoolname)

    def post(self, request, *args, **kwargs):
        self.get_queryset()
        return self.list(request, *args, **kwargs)


class ClassCreateView(ListAPIView):
    """
    创建一个班级
    """
    model = Class
    permission_classes = (permissions.AllowAny, )
    serializer_class = ClassCreateSerializer

    def post(self, request):
        serializer = ClassCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={'code': '0', 'message': 'Success!'}, status=status.HTTP_201_CREATED)
        else:
            return Response("Error!", status=status.HTTP_400_BAD_REQUEST)


