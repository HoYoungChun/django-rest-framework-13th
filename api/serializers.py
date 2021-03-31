from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    heart_post = HeartSerializer(many=True, read_only=True)
    file_post = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    _following = FollowSerializer(many=True, read_only=True)
    _followed = FollowSerializer(many=True, read_only=True)
    _user = HeartSerializer(many=True, read_only=True)
    _author = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['nickname', 'email', 'phone_number', 'password', 'username', 'description', 'created_at', 'updated_at']

