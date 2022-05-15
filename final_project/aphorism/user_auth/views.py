from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import UserRegForm, UserLoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout



class RegisterUser(CreateView):
    form_class = UserRegForm
    template_name = 'register.html'
    success_url = reverse_lazy('user_auth:login')


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('scrap:get_aphs')


def user_logout(request):
    logout(request)
    return redirect('scrap:get_aphs')
