from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_categories', default=1)

    def __str__(self):
        return self.name


class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    class DraftObject(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='draft')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1, related_name='blog_categ')
    title = models.CharField(max_length=250)
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')
    excerpt = models.TextField(null=True)
    content = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=options, default='published')
    objects = models.Manager()
    postObjects = PostObjects()
    draftObjects = DraftObject()

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title


class Viewer(models.Model):
    post = models.ForeignKey(Post, related_name='views', on_delete=CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users_comment')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users_like')
    date = models.DateTimeField(auto_now_add=True)
