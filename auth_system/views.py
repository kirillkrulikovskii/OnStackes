from typing import Any

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, FormView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, login_not_required, user_passes_test


from . import models as auth_models
from . import forms  as auth_forms

class RegView(TemplateView):
    template_name = "auth/register_login"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

def reg_login(request):
    if request.method == "POST": # register
        pass
    elif request.method == "GET": # login
        pass 

    return render(request, "auth/register_login.html", {})

