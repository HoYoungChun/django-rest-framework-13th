from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.all()

class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()

class FileViewSet(viewsets.ModelViewSet):
	serializer_class = FileSerializer
	queryset = File.objects.all()

class FollowViewSet(viewsets.ModelViewSet):
	serializer_class = FollowSerializer
	queryset = Follow.objects.all()

class HeartViewSet(viewsets.ModelViewSet):
	serializer_class = HeartSerializer
	queryset = Heart.objects.all()