from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .forms import (UserForm, LoginUserForm, NewPostForm, ContactForm,
                    UserProfileForm, AdminProfileForm, OldPasswordChangeForm)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Post
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail, BadHeaderError


# Home page
def home_page(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


# Sign up page
def signup_page(request):
    if request.method == 'POST':
        fm = UserForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Congrats!! you become an Author. Please log in now.')
            user = fm.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        fm = UserForm()
    return render(request, 'blog/signup.html', {'form': fm})


# Log in page
def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginUserForm(request=request, data=request.POST)
            if fm.is_valid():
                un = fm.cleaned_data['username']
                ps = fm.cleaned_data['password']
                user = authenticate(username=un, password=ps)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully. Hello User! Welcome here...')
                    return HttpResponseRedirect('/dash/')
        else:
            fm = LoginUserForm()
        return render(request, 'blog/login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/dash/')


# Dashboard page
def dashboard_page(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        groups = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': groups})
    else:
        return HttpResponseRedirect('/login/')


# Add new Blog here
def add_blog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = NewPostForm(request.POST)
            if fm.is_valid():
                tm = fm.cleaned_data['title']
                ds = fm.cleaned_data['descript']
                pst = Post(title=tm, descript=ds)
                pst.save()
                fm = NewPostForm()
        else:
            fm = NewPostForm()
        return render(request, 'blog/add.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


# Blog update page
def update_blog(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            fm = NewPostForm(request.POST, instance=pi)
            if fm.is_valid():
                fm.save()
        else:
            pi = Post.objects.get(pk=id)
            fm = NewPostForm(instance=pi)
        return render(request, 'blog/update.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


# Delete blog here
def delete_blog(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dash/')
    else:
        return HttpResponseRedirect('/login/')


# Log out page
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login/')


# Profile Page for user and Admin
def profile_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if user.is_superuser == True:
                fm = AdminProfileForm(request.POST, instance=request.user)
                users = User.objects.all()
                posts = Post.objects.all()
            else:
                fm = UserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                messages.success(request, 'profile updated...!!')
                fm.save()
        else:
            if request.user.is_superuser == True:
                fm = AdminProfileForm(instance=request.user)
                users = User.objects.all()
                posts = Post.objects.all()
                pst = 0
                for p in posts:
                    pst = pst + 1

            else:
                fm = UserProfileForm(instance=request.user)
                users = None
                pst = None
        return render(request, 'blog/profile.html', {'form': fm, 'users': users, 'post': pst})
    else:
        return HttpResponseRedirect('/login/')


# This function give user's detail to admin
def user_detail(request, id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        fm = AdminProfileForm(instance=pi)
        return render(request, 'blog/user_detail.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


# Admin can delete users from admin profile
def delete_user(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = User.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/profile/')
    else:
        return HttpResponseRedirect('/login/')


# About Page
def about_page(request):
    return render(request, 'blog/about.html')


# Contact Page
def contact_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = ContactForm(request.POST)
            if fm.is_valid():
                subject = fm.cleaned_data['subject']
                body = {
                    'first_name': fm.cleaned_data['first_name'],
                    'last_name': fm.cleaned_data['last_name'],
                    'email': fm.cleaned_data['email'],
                    'message': fm.cleaned_data['message']
                }
                message = "\n".join(body.values())
                try:
                    send_mail(subject, message, 'webshine71@gmail.com', ['webshine71@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return HttpResponseRedirect('/contact/')
        else:
            fm = ContactForm()
        return render(request, 'blog/contact.html', {'form': fm})
    else:
        fm = ContactForm()
        return render(request, 'blog/contact.html', {'form': fm})


# user can change password with old password
def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = OldPasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                return HttpResponseRedirect('/profile/')
        else:
            fm = OldPasswordChangeForm(user=request.user)
        return render(request, 'blog/with_old.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')
