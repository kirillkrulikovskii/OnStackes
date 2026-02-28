from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, FormView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, login_not_required, user_passes_test # type: ignore
from typing import Any


from . import models as auth_models
from . import forms  as auth_forms


# register_login.html

@login_not_required
def register_login(request):
    if request.method == 'POST':
        if 'login' in request.POST: # Check if the login form is submitted
            login_form = auth_forms.LoginForm(request.POST)
            register_form = auth_forms.RegisterForm()
            print('Login form submitted')
            if login_form.is_valid(): # invalid why? i check if the user exists and if the password is correct in the clean method of the form. but it is still invalid. maybe because of the email field? but i removed it. maybe because of the username field? but i kept it. maybe because of the password field? but i kept it. maybe because of the form itself? but i don't know why. maybe because of the csrf token? but i have it in the template. maybe because of the action url? but i have it in the template. maybe because of something else? but i don't know what else could be wrong.
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                email = '@' in str(username) and username or None # Check if the input is an email or a username
                user = auth_models.Accounts.objects.get(username=username) if not email else auth_models.Accounts.objects.get(email=email)
                print('User found:', user)
                print('Username  :', username)
                print('email     :', email)
                print('Password  :', password)
                if user.check_password(password):
                    from django.contrib.auth import login
                    login(request, user)
                    print('Succefully logged in!')
                    return redirect('home')
        elif 'register' in request.POST: # Check if the register form is submitted
            register_form = auth_forms.RegisterForm(request.POST)
            login_form = auth_forms.LoginForm()
            if register_form.is_valid():
                username = register_form.cleaned_data['username']
                email = register_form.cleaned_data['email']
                password = register_form.cleaned_data['password']
                user = auth_models.Accounts.objects.create_user(username=username, email=email, password=password)
                from django.contrib.auth import login
                login(request, user)
                print('Succefully registered and logged in!')
                return redirect('home')
    else:
        login_form = auth_forms.LoginForm()
        register_form = auth_forms.RegisterForm()

    return render(request, 'auth/register_login.html', {
        'login_form': login_form,
        'register_form': register_form
    })

# register_login.html was problem because action could not open the view.

def profile_view(request, pk): # User's id is passed as pk
    forms = auth_forms.ProfileEditedForm()
    if request.user.id == pk and request.method == 'POST': # User is editing their own profile not others' profile
        forms = auth_forms.ProfileEditedForm(request.POST, request.FILES, instance=request.user)
        if forms.is_valid():
            forms.save()
            return redirect('auth_system:profile', pk=pk)
    user = get_object_or_404(auth_models.Accounts, pk=pk)
    return render(request, 'auth_system/profile.html', {'pk': pk, 'user': user, 'form': forms})
