import datetime
from django.db import models
from django.contrib.auth.models import User


class myUser(User):
    birthday = models.DateField(null=True)
    profile_pic = models.FileField(upload_to="Profiles", null=True, blank=True)
    cover_pic = models.FileField(upload_to="Covers", null=True, blank=True)
    follower = models.ManyToManyField(User, related_name="follower")
    following = models.ManyToManyField(User, related_name="following")
    male = models.BooleanField(default=True)


class Movie(models.Model):
    name = models.CharField(max_length=50)
    poster = models.FileField(upload_to="Posters", null=True, blank=True)
    cover = models.FileField(upload_to="covers", null=True, blank=True)
    desc = models.TextField(blank=True, null=True)
    link = models.URLField(default='https://google.com')
    director = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    stars = models.TextField(max_length=100, default='Cristian Bale')
    music = models.CharField(max_length=50)
    rel_date = models.DateField(auto_now_add=True, blank=True)
    run_time = models.IntegerField(default=100)
    rate = models.IntegerField(default=9)
    rating = models.IntegerField(default=9)


class Post(models.Model):
    author = models.ForeignKey(myUser, related_name="p_author")
    date = models.DateTimeField(default=datetime.datetime.now)
    movie = models.ForeignKey(Movie, related_name="p_movie")
    text = models.TextField(blank=True)


class Like(models.Model):
    author = models.ForeignKey(myUser, related_name="l_author")
    post = models.ForeignKey(Post, related_name="l_post")
    date = models.DateTimeField(auto_now_add=True, blank=True)


class Comment(models.Model):
    author = models.ForeignKey(myUser, related_name="c_author")
    post = models.ForeignKey(Post, related_name="c_post")
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(myUser, related_name="user")
    desc = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.datetime.now)


class RoleTable(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    movie = models.ForeignKey(Movie, related_name="r_movie")