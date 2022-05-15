from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Authors, Quotas, Tags
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import SearchForm


class AphListView(ListView):
    model = Quotas
    paginate_by = 10
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context

    def get_queryset(self):
        object_list = Quotas.objects.all()
        if 'quota' in self.request.GET and self.request.GET['quota']:
            quota = self.request.GET['quota']
            object_list = object_list.filter(quota__icontains=quota)

        if 'author' in self.request.GET and self.request.GET['author']:
            author = self.request.GET['author']

            object_list = object_list.filter(author=author)

        if 'tag' in self.request.GET and self.request.GET['tag']:
            tag = self.request.GET['tag']
            object_list = object_list.filter(tag=tag)

        if 'user' in self.request.GET and self.request.GET['user']:
            user = self.request.GET['user']
            object_list = object_list.filter(user=user)

        return object_list


class AphView(DetailView):
    model = Quotas
    template_name = 'aph.html'


class AddAph(LoginRequiredMixin, CreateView):
    model = Quotas
    fields = ('quota', 'tag')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add quote'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        auth = f'{self.request.user.first_name} {self.request.user.last_name}'
        a, _ = Authors.objects.get_or_create(author=auth)
        form.instance.author = a
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('scrap:get_aphs')


class UpdateAph(LoginRequiredMixin, UpdateView):
    model = Quotas
    fields = ('quota', 'tag')
    template_name_suffix = '_update_form'

    def get_queryset(self):
        object_list = Quotas.objects.filter(user=self.request.user)
        return object_list

    def get_success_url(self):
        return reverse('scrap:aph', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'update quote'
        return context


class DeleteAph(DeleteView):
    model = Quotas
    success_url = reverse_lazy('scrap:get_aphs')

    def form_valid(self, form):
        q=Quotas.objects.filter(user=self.request.user).all()
        if len(q)<2:
            Authors.objects.filter(author=q[0].author).delete()
        return super().form_valid(form)

    def get_queryset(self):
        object_list = Quotas.objects.filter(user=self.request.user)

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete quote'
        return context
