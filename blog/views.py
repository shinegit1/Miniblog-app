from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import (UserForm, LoginUserForm, NewPostForm, ContactForm,
                    UserProfileForm, AdminProfileForm, OldPasswordChangeForm)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Post
from django.contrib.auth.models import User
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
            fm.save()
            un = fm.cleaned_data['username']
            ps = fm.cleaned_data['password1']
            user = authenticate(username=un, password=ps)
            if user is not None:
                login(request, user)
                messages.success(request, 'Congrats!! your account created. Please log in now.')
                return HttpResponseRedirect('/dash/')
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
                    messages.success(request, 'Logged in successfully. Hello Author! Welcome here.')
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
        full_name = request.user.get_full_name()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name': full_name})
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
                pst = Post(user=request.user, title=tm, descript=ds)
                pst.save()
                messages.success(request, 'Your blog is created successfully.')
                fm = NewPostForm()
        else:
            fm = NewPostForm()
        return render(request, 'blog/add.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


# Blog update page
def update_blog(request, user_id: int):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=user_id)
            fm = NewPostForm(request.POST, instance=pi)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Your blog is updated successfully.')
        else:
            pi = Post.objects.get(pk=user_id)
            fm = NewPostForm(instance=pi)
        return render(request, 'blog/update.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


# Delete blog here
def delete_blog(request, user_id: int):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=user_id)
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
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            if user.is_superuser:
                fm = AdminProfileForm(request.POST, instance=user)
                users = User.objects.all()
                posts = Post.objects.all()
            else:
                fm = UserProfileForm(request.POST, instance=user)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'profile updated...!!')
        else:
            if user.is_superuser:
                fm = AdminProfileForm(instance=user)
                users = User.objects.all()
                posts = Post.objects.all()
                pst = 0
                for p in posts:
                    pst = pst + 1

            else:
                fm = UserProfileForm(instance=user)
                users = None
                pst = None
        return render(request, 'blog/profile.html', {'form': fm, 'users': users, 'post': pst})
    else:
        return HttpResponseRedirect('/login/')


# This function give user's detail to admin
def user_detail(request, user_id: int):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=user_id)
        fm = AdminProfileForm(instance=pi)
        return render(request, 'blog/user_detail.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


# Admin can delete users from admin profile
def delete_user(request, user_id: int):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = User.objects.get(pk=user_id)
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
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            fm = OldPasswordChangeForm(user=user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                return HttpResponseRedirect('/profile/')
        else:
            fm = OldPasswordChangeForm(user=user)
        return render(request, 'blog/with_old.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')
