import uuid
from .models import *
from django import forms
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.forms.extras import SelectDateWidget
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from captcha.fields import CaptchaField


class ResetForm(forms.Form):
    mail = forms.EmailField()


class LoginForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = myUser
        fields = ['username', 'password']


class SignUpForm(forms.ModelForm):
    confirm_password = forms.PasswordInput()
    captcha = CaptchaField()
    birthday = forms.DateField(widget=SelectDateWidget(years=range(datetime.date.today().year, 1930, -1)))

    class Meta:
        model = myUser
        fields = ['username', 'password', 'first_name', 'last_name', 'birthday', 'email', 'male', 'profile_pic',
                  'cover_pic']


def handle_uploaded_file(f):
    name = 'media/%s.jpg' % uuid.uuid1()
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def my_login(request):
    wup = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("/timeline/")
            else:
                wup = True
    else:
        form = LoginForm()

    return render(request, "login.html", {'form': form, 'wup': wup})


def my_logout(request):
    logout(request)
    return render(request, "login.html")


def signup(request):
    thank = ""
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            birthday = form.cleaned_data['birthday']
            male = form.cleaned_data['male']
            profile_pic = form.cleaned_data['profile_pic']
            cover_pic = form.cleaned_data['cover_pic']
            handle_uploaded_file(request.FILES['profile_pic'])
            handle_uploaded_file(request.FILES['cover_pic'])
            user = myUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, birthday=birthday, male=male,
                                              profile_pic=profile_pic, cover_pic=cover_pic)

            thank = "Thanks for your singing up, "+user.first_name+" !! :D"
            user.save()
    else:
        form = SignUpForm()
    return render(request, "login.html", {'form': form, 'thank': thank})


def forgot(request):
    return render(request, "forget.html")


def reset(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            mail = request.POST.get('mail', None)
            send_mail('Reset Password', 'You have received this email because you want to reset your password.',
                      'admin@admin.com', [mail], fail_silently=False)
    else:
        form = ResetForm()
        raise forms.ValidationError("Please enter a valid email address!")
    return render(request, "forget.html", {'form': form})


@login_required(function=None, login_url="/login/")
def change(request, username):
    user = myUser.objects.get(username=username)
    return render(request, "profile.html")



@login_required(function=None, login_url="/login/")
def movie(request, name):
    m = Movie.objects.get(name=name)
    return render(request, "movie.html", {'m': m})


@login_required(function=None, login_url="/login/")
def profile(request, username):
    p = myUser.objects.get(username=username)
    post_num = Post.objects.filter(author__username=username).count()
    ers_num = p.follower.count()
    ing_num = p.following.count()
    return render(request, "profile.html", {'p': p, 'post_num': post_num, 'ers_num': ers_num, 'ing_num': ing_num})

"""
def infinite_scroll(request):
    return render(request, "profile.html")
"""

@login_required(function=None, login_url="/login/")
def timeline(request):
    fav_movies = Movie.objects.all()[0:2]
    sug_people = myUser.objects.all()[0:2]
    sug_movies = Movie.objects.all()[0:2]

    posts = Post.objects.all()[0:2]

    return render(request, "timeline.html", {'fav_movies': fav_movies, 'sug_movies': sug_movies,
                                             'sug_people': sug_people, 'posts': posts})


@login_required(function=None, login_url="/login/")
def posts(request, post_id):
    tpost = Post.objects.get(id=post_id)
    fav_movies = Movie.objects.all()[0:2]
    sug_people = myUser.objects.all()[0:2]
    sug_movies = Movie.objects.all()[0:2]

    return render(request, "post.html", {'fav_movies': fav_movies, 'sug_movies': sug_movies, 'sug_people': sug_people,
                                         'tpost': tpost})


def post(request, name):
    cur_user = None
    if request.user.is_authenticated():
        cur_user = request.user.username
    user = myUser.objects.get(username=cur_user)
    mov = Movie.objects.get(name=name)

    po = Post.objects.create(author=user, date=datetime.datetime.now, movie=mov, )
    po.save()
    return render(request, "timeline.html")


def like(request, post_id):
    cur_user = None
    if request.user.is_authenticated():
        cur_user = request.user.username
    l = Like.objects.create(author=myUser.objects.get(username=cur_user), post=Post.objects.get(id=post_id),
                            date=datetime.datetime.now)
    l.save()
    return HttpResponse("ok")


def comment(request, post_id):
    text = request.POST.get('text')
    cur_user = None
    if request.user.is_authenticated():
        cur_user = request.user.username
    c = Comment.objects.create(author=myUser.objects.get(username=cur_user), post=Post.objects.get(id=post_id),
                               text=text, date=datetime.datetime.now)
    c.save()
    return HttpResponse("ok")


