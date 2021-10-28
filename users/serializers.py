from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import NewUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['id'] = self.user.id
        data['username'] = self.user.user_name
        return data


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'first_name', 'about', 'profile')


class MyProfileSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)

    def get_posts(self, obj):
        return obj.blog_posts.count()

    def get_likes(self, obj):
        likes = 0
        for post in obj.blog_posts.all():
            likes = likes + post.likes.count()
        return likes

    def get_views(self, obj):
        views = 0
        for post in obj.blog_posts.all():
            views = views + post.views.count()
        return views

    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'first_name', 'about', 'profile', 'posts', 'likes', 'views')
