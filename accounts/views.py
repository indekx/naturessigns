from django.shortcuts import render
from django.contrib import messages
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import View
from django.views import generic
from django.contrib.auth import login as auth_login
from django.contrib import messages
from accounts.forms import SignUpForm, UserLoginForm,EditProfileForm, ChangePasswordForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # Further validation
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 
             "Thank you! Your account has been successfully createdt."
            )

            return redirect('index')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)

            if 'next' in request.POST:

                return redirect(request.POST.get('next'))

            else:

                return redirect('index')

        else:
            form = UserLoginForm()

        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('index')


def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/view_profile.html', args)


# Edit profile view
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile was updated successfully')
            return redirect('view_profile')
        
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

# Password change view
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('change_password')
       
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
    

def password_reset_done(request):
    return render(request, 'accounts/reset_password_confirm')
