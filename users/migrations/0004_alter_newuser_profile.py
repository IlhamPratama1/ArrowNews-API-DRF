# Generated by Django 3.2.6 on 2021-10-14 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_newuser_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='profile',
            field=models.ImageField(default='posts/ava.jpg', upload_to='posts/', verbose_name='Profile'),
        ),
    ]