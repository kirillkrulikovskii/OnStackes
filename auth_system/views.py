from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, FormView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from typing import Any


from . import models as auth_models
from . import forms  as auth_forms


# register_login.html

@login_required
def register_login(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = auth_forms.LoginForm(request.POST)
            register_form = auth_forms.RegisterForm()
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                user = auth_models.Accounts.objects.get(email=email)
                if user.check_password(password):
                    from django.contrib.auth import login
                    login(request, user)
                    return redirect('home')
        elif 'register' in request.POST:
            register_form = auth_forms.RegisterForm(request.POST)
            login_form = auth_forms.LoginForm()
            if register_form.is_valid():
                username = register_form.cleaned_data['username']
                email = register_form.cleaned_data['email']
                password = register_form.cleaned_data['password']
                user = auth_models.Accounts.objects.create_user(username=username, email=email, password=password)
                from django.contrib.auth import login
                login(request, user)
                return redirect('home')
    else:
        login_form = auth_forms.LoginForm()
        register_form = auth_forms.RegisterForm()

    return render(request, 'auth_system/register_login.html', {
        'login_form': login_form,
        'register_form': register_form
    })

def profile_view(request, pk): # User's id is passed as pk
    forms = auth_forms.ProfileEditedForm()
    if request.user.id == pk and request.method == 'POST': # User is editing their own profile not others' profile
        forms = auth_forms.ProfileEditedForm(request.POST, request.FILES, instance=request.user)
        if forms.is_valid():
            forms.save()
            return redirect('auth_system:profile', pk=pk)
    user = get_object_or_404(auth_models.Accounts, pk=pk)
    return render(request, 'auth_system/profile.html', {'pk': pk, 'user': user, 'form': forms})
