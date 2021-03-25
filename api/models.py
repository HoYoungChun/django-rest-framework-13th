from django.db import models


# Create your models here.

class User(models.Model):
    # 닉네임, 이메일, 전화번호로 로그인하기 때문에 Unique해야
    nickname = models.CharField(max_length=100, verbose_name="닉네임", unique=True)
    email = models.EmailField(max_length=255, verbose_name="이메일", unique=True)
    phone_number = models.CharField(max_length=100, verbose_name="전화번호", unique=True)

    password = models.CharField(max_length=150, verbose_name="비밀번호", unique=True)
    username = models.CharField(max_length=150, verbose_name="이름", unique=True)
    description = models.TextField(verbose_name="소개")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="가입일자")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="업데이트일자")


class Post(models.Model):
    title = models.CharField(max_length=200)
