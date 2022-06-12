from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import UserRegForm, UserLoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from scrap.models import UsersPhotos


class RegisterUser(CreateView):
    form_class = UserRegForm
    template_name = 'register.html'
    success_url = reverse_lazy('accounts:login')


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('scrap:get_aphs')


def user_logout(request):
    logout(request)
    return redirect('scrap:get_aphs')


@login_required
def settings(request):
    data={}
    data['photos'] = UsersPhotos.objects.filter(user_photo=request.user).all()
    return render(request, 'registration/acc_settings.html',data)
