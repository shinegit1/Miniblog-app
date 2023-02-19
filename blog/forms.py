from .models import Post, Contact
from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm, UsernameField, \
    UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _


class UserForm(UserCreationForm):
    # This is user form for sign up page
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {'email': 'Email-ID'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class LoginUserForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'strip': False,
                                                                 'autocomplete': 'current-password'}))


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'descript']
        labels = {'title': 'Title', 'descript': 'Description'}
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'descript': forms.Textarea(attrs={'class': 'form-control'}),
                   }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AdminProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'user_permissions': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'date_joined': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'last_login': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }


class UserProfileForm(AdminProfileForm):
    password = None

    class Meta(AdminProfileForm.Meta):
        fields = ['first_name', 'last_name', 'username', 'email', 'date_joined', 'last_login']


class OldPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autofocus': True, 'class': 'form-control', 'required': 'true'}),
                                   )
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autofocus': True, 'class': 'form-control', 'required': 'true'}),
                                    )
    new_password2 = forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autofocus': True, 'class': 'form-control', 'required': 'true'}),
                                    )
