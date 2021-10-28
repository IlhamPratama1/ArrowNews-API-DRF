# Generated by Django 3.2.6 on 2021-09-09 01:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_post_viewer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='viewer',
        ),
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='blog.post')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_like', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='blog.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_comment', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
        ),
    ]