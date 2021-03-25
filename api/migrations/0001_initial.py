# Generated by Django 3.1.7 on 2021-03-25 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100, unique=True, verbose_name='닉네임')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='이메일')),
                ('phone_number', models.CharField(max_length=100, unique=True, verbose_name='전화번호')),
                ('password', models.CharField(max_length=150, unique=True, verbose_name='비밀번호')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='이름')),
                ('description', models.TextField(verbose_name='소개')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='가입일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='업데이트일자')),
            ],
        ),
    ]
