from rest_framework import serializers

from blog.models import Category, Comment, Like, Post, Viewer


class CategorySerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)

    def get_posts(self, obj):
        return obj.blog_categ.count()

    def get_likes(self, obj):
        likes = 0
        for post in obj.blog_categ.all():
            likes = likes + post.likes.count()
        return likes

    def get_views(self, obj):
        views = 0
        for post in obj.blog_categ.all():
            views = views + post.views.count()
        return views

    class Meta:
        model = Category
        fields = ('id', 'name', 'posts', 'likes', 'views')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class ViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewer
        fields = ('id', )


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text')


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True, source="author.user_name")
    author_image = serializers.SerializerMethodField()

    def get_author_image(self, post):
        request = self.context.get('request')
        author_image = 'https://arrownews-api-drf.herokuapp.com/media/' + str(post.author.profile)
        return request.build_absolute_uri(author_image)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author_name', 'author_image', 'text', 'created_date')


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.CharField(read_only=True, source='category.name')
    author_name = serializers.CharField(read_only=True, source="author.user_name")
    author_image = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_views(self, obj):
        return obj.views.count()

    def get_comments(self, obj):
        return obj.comments.count()

    def get_author_image(self, post):
        request = self.context.get('request')
        author_image = 'https://arrownews-api-drf.herokuapp.com/media/' + str(post.author.profile)
        return request.build_absolute_uri(author_image)

    class Meta:
        model = Post
        fields = ('category', 'category_name', 'id', 'title', 'image', 'slug', 'author', 'author_name', 'author_image', 'published',
                  'excerpt', 'content', 'status', 'comments', 'likes', 'views')


class PostAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('category', 'id', 'title', 'image', 'slug', 'author',
                  'excerpt', 'content', 'status')
