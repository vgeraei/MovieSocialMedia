# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('text', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('poster', models.FileField(upload_to='Posters', null=True, blank=True)),
                ('cover', models.FileField(upload_to='covers', null=True, blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('link', models.URLField(default='https://google.com')),
                ('director', models.CharField(max_length=50)),
                ('producer', models.CharField(max_length=50)),
                ('stars', models.TextField(max_length=100, default='Cristian Bale')),
                ('music', models.CharField(max_length=50)),
                ('rel_date', models.DateField(auto_now_add=True)),
                ('run_time', models.IntegerField(default=100)),
                ('rate', models.IntegerField(default=9)),
                ('rating', models.IntegerField(default=9)),
            ],
        ),
        migrations.CreateModel(
            name='myUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL, parent_link=True)),
                ('profile_pic', models.FileField(upload_to='Profiles', null=True, blank=True)),
                ('cover_pic', models.FileField(upload_to='Covers', null=True, blank=True)),
                ('male', models.BooleanField(default=True)),
                ('follower', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='follower')),
                ('following', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='following')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('desc', models.CharField(max_length=100)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(related_name='user', to='ourapp.myUser')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('text', models.TextField(blank=True)),
                ('author', models.ForeignKey(related_name='p_author', to='ourapp.myUser')),
                ('movie', models.ForeignKey(related_name='p_movie', to='ourapp.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='RoleTable',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50)),
                ('movie', models.ForeignKey(related_name='r_movie', to='ourapp.Movie')),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='author',
            field=models.ForeignKey(related_name='l_author', to='ourapp.myUser'),
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(related_name='l_post', to='ourapp.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(related_name='c_author', to='ourapp.myUser'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='c_post', to='ourapp.Post'),
        ),
    ]
