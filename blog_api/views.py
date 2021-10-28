from django.db.models import Count
from django.http import Http404
from rest_framework import filters, generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Category, Comment, Like, Post

from .paginations import CategoryPagination, CustomPagination
from .serializers import (CategorySerializer, CommentPostSerializer,
                          CommentSerializer, LikeSerializer,
                          PostAdminSerializer, PostSerializer,
                          ViewerSerializer)


class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    queryset = Post.postObjects.all()


class TopPostList(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    queryset = Post.objects.annotate(num_views=Count('views')).order_by('-num_views')


class PostDetail(generics.RetrieveAPIView):
    serializer_class = PostSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)


class PostListDetailFillter(generics.ListAPIView):
    search_fields = ['title']
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [filters.SearchFilter]
    pagination_class = CategoryPagination


class PostbyCategory(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = CategoryPagination

    def get_queryset(self, **kwargs):
        categ_slug = self.kwargs.get('pk')
        categ = Category.objects.get(name=categ_slug)
        return Post.objects.filter(category=categ)


class PostComments(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self, **kwargs):
        post_slug = self.kwargs.get('pk')
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)


class PostViews(generics.CreateAPIView):
    serializer_class = ViewerSerializer

    def get_post(self, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        post = self.get_post(self.request.data.get('slug'))
        serializer.save(post=post)


class PostCommentUser(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentPostSerializer


class AdminPostCategory(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer


class PostLikeUser(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def get_post(self, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        post = self.get_post(self.kwargs.get('pk'))
        user = self.request.user
        like = Like.objects.filter(author=user, post=post)

        if not like:
            serializer.save(author=user, post=post)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetLikeUser(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def get_post(self, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404

    def get_queryset(self, **kwargs):
        post = self.get_post(self.kwargs.get('pk'))
        return Like.objects.filter(author=self.request.user, post=post)


# -------------ADMIN----------- #
class AdminPostList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)


class AdminDraftList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.draftObjects.filter(author=user)


class AdminCategoryList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(num_posts=Count('blog_categ')).order_by('-num_posts')


class CreatePost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, format=None):
        serializer = PostAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPostDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class EditPost(generics.UpdateAPIView, PostUserWritePermission):
    permission_classes = [permissions.IsAuthenticated, PostUserWritePermission]
    serializer_class = PostAdminSerializer
    queryset = Post.objects.all()


class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostAdminSerializer
    queryset = Post.objects.all()
