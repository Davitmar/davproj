import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, HttpResponseRedirect
from .models import Authors, Quotas, Tags, Messege, UsersPhotos, Friends
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import SearchForm, MessegeSearchForm, UserSearchForm
from django.contrib.auth.models import User


class AphListView(ListView):
    model = Quotas
    paginate_by = 10
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context

    def get_queryset(self):
        object_list = Quotas.objects.all().order_by('-date')

        if 'quota' in self.request.GET and self.request.GET['quota']:
            quota = self.request.GET['quota']
            object_list = object_list.filter(quota__icontains=quota)

        if 'author' in self.request.GET and self.request.GET['author']:
            author = self.request.GET['author']
            object_list = object_list.filter(author=author)

        if 'tag' in self.request.GET and self.request.GET['tag']:
            tag = self.request.GET['tag']
            object_list = object_list.filter(tag=tag)

        if 'user' in self.request.GET:
            object_list = object_list.filter(user=self.request.user)

        if 'fav' in self.request.GET:
            # fav = self.request.GET['fav']
            object_list = object_list.filter(fav=self.request.user)

        return object_list


class AphView(DetailView):
    model = Quotas
    template_name = 'aph.html'


class AddAph(LoginRequiredMixin, CreateView):
    model = Quotas
    fields = ('quota', 'tag', 'picture')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add quote'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.user.first_name:
            auth = f'{self.request.user.first_name} {self.request.user.last_name}'
            a, _ = Authors.objects.get_or_create(author=auth)
            form.instance.author = a
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('scrap:get_aphs')


class UpdateAph(LoginRequiredMixin, UpdateView):
    model = Quotas
    fields = ('quota', 'tag', 'picture')
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


class DeleteAph(LoginRequiredMixin, DeleteView):
    model = Quotas
    success_url = reverse_lazy('scrap:get_aphs')

    def form_valid(self, form):
        success_url = self.get_success_url()
        q = Quotas.objects.filter(user=self.request.user).all()
        if len(q) < 2:
            Authors.objects.filter(author=q[0].author).delete()
        if self.object.picture:
            file_path = os.getcwd() + f'/media/{self.object.picture}'
            os.remove(file_path)
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_queryset(self):
        object_list = Quotas.objects.filter(user=self.request.user)

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete quote'
        return context


def fav_add(request, i):
    quote = get_object_or_404(Quotas, id=i)

    if quote.fav.filter(id=request.user.id).exists():
        quote.fav.remove(request.user)
    else:
        quote.fav.add(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


'''messege send implementation 128-'''


class SendMes(LoginRequiredMixin, CreateView):
    model = Messege
    fields = ('messege', 'nkar')
    success_url = reverse_lazy('scrap:mess')


    @staticmethod
    def f(req):
        q = req.GET['rec']
        if q.replace(req.user.username, ''):
            f = q.replace(req.user.username, '')
        else:
            f = req.user.username
        return f

    def form_valid(self, form):
        if form.instance.messege or form.instance.nkar:
            f = self.f(self.request)
            rec = get_object_or_404(User, username=f)
            form.instance.sender = self.request.user
            form.instance.reciever = rec
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(self.request.META["HTTP_REFERER"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        f = self.f(self.request)
        context['rec'] = self.f(self.request)
        obj = Messege.objects.filter(Q(reciever=self.request.user, sender__username=f) |
                                     Q(sender=self.request.user, reciever__username=f)).order_by('date')
        context['object_list'] = obj
        return context

    def get_success_url(self):
        return self.success_url + '?rec=' + self.object.sender.username + self.object.reciever.username


class Sentes(LoginRequiredMixin, ListView):
    model = Messege
    paginate_by = 10
    template_name = 'user_messeges.html'

    def get_queryset(self):
        object_list = Messege.objects.filter(
            Q(reciever=self.request.user) | Q(sender=self.request.user)).order_by('-date')
        if 'sender' in self.request.GET and self.request.GET['sender']:
            sender = self.request.GET['sender']
            object_list = object_list.filter(
                ((Q(reciever__username__contains=sender) | Q(reciever__first_name__contains=sender))
                 & ~Q(reciever=self.request.user)) | (
                        (Q(sender__username__contains=sender) | Q(reciever__first_name__contains=sender))
                        & ~Q(sender=self.request.user)))

        l = []
        m = []
        for i in object_list:
            if i.sender == self.request.user and i.reciever not in l:
                l.append(i.reciever)
                m.append(i)
            elif i.sender != self.request.user and i.sender not in l:
                l.append(i.sender)
                m.append(i)

        object_list = m

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = MessegeSearchForm()
        return context


class Sms(LoginRequiredMixin, ListView):
    model = Messege
    paginate_by = 10
    template_name = 'sms_messeges.html'

    def get_queryset(self):
        q = self.request.GET['param']
        if q.replace(self.request.user.username, ''):
            f = q.replace(self.request.user.username, '')
        else:
            f = self.request.user.username
        object_list = Messege.objects.filter(Q(reciever=self.request.user, sender__username=f) |
                                             Q(sender=self.request.user, reciever__username=f)).order_by('-date')

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other'] = self.request.GET['param']
        return context


class DeleteMes(LoginRequiredMixin, DeleteView):
    model = Messege
    success_url = reverse_lazy('scrap:mess')

    def get_queryset(self):
        object_list = Messege.objects.filter(
            Q(reciever=self.request.user) | Q(sender=self.request.user))
        return object_list

    def form_valid(self, form):
        success_url = self.get_success_url()
        if self.object.nkar:
            file_path = os.getcwd() + f'/media/{self.object.nkar}'
            os.remove(file_path)
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return self.success_url + '?rec=' + self.object.sender.username + self.object.reciever.username


# object_list=User.objects.filter(Q(send__reciever=self.request.user) |
# Q(reciev__sender=self.request.user)).order_by('-send__date')#.distinct()

#data['requests'] = User.objects.filter(f_s__friend_reciever=request.user).all(),
#sa /f_s related_name na Friends um u User objecta/ nshanakuma request uxarkac user/ nshanakuma ayn usernery /User/-ic, voronc hamapatasxan friend_reciever /Friends/-um havasara request.user in

'''users search form, users photos, accounts'''


class UsersList(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 10
    template_name = 'users_list.html'


    def get_queryset(self):
        object_list = User.objects.all()

        if 'username' in self.request.GET:
            search_query = self.request.GET['username']
            object_list = object_list.filter(Q(username__icontains=search_query) |
                                             Q(first_name__icontains=search_query) |
                                             Q(last_name__icontains=search_query))

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_photos'] = UsersPhotos.objects.filter(is_main=True).all()
        context['search_form'] = UserSearchForm
        context['friend'] = Friends.objects.filter(
            Q(friend_reciever=self.request.user) | Q(friend_sender=self.request.user)).all()



        return context


class UserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'one_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['one_user_photos'] = UsersPhotos.objects.filter(user_photo=self.object).all()
        context['quotas'] = Quotas.objects.filter(user=self.object).all()
        context['friend'] = Friends.objects.filter(Q(friend_reciever=self.request.user, friend_sender=self.object.id) | Q(friend_reciever=self.object.id, friend_sender=self.request.user)).first()

        return context


class AddPhoto(LoginRequiredMixin, CreateView):
    model = UsersPhotos
    fields = ('image', )

    # template_name = 'addphoto.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Add quote'
    #     return context

    def form_valid(self, form):
        form.instance.user_photo = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:settings')


@login_required
def set_main(request, j):
    new_main = get_object_or_404(UsersPhotos, user_photo=request.user, id=j)

    if UsersPhotos.objects.filter(user_photo=request.user, is_main=True):
        old_main = get_object_or_404(UsersPhotos, user_photo=request.user, is_main=True)
        old_main.is_main = False
        old_main.save()
    new_main.is_main = True
    new_main.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name')
    template_name_suffix = '_change_form'

    def get_queryset(self):
        object_list = list(self.request.user)
        return object_list

    def get_success_url(self):
        return reverse('scrap:aph', args=[self.object.id])

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'update quote'
    #     return context


class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('scrap:get_aphs')

    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     q = Quotas.objects.filter(user=self.request.user).all()
    #     if len(q) < 2:
    #         Authors.objects.filter(author=q[0].author).delete()
    #     file_path = os.getcwd() + f'/media/{self.object.picture}'
    #     os.remove(file_path)
    #     self.object.delete()
    #     return HttpResponseRedirect(success_url)

    def get_queryset(self):
        object_list = list(self.request.user)
        return object_list

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'delete quote'
    #     return context


@login_required
def delete_photo(request, i):
    del_photo = get_object_or_404(UsersPhotos, id=i, user_photo=request.user)

    file_path = os.getcwd() + f'/media/{del_photo.image}'
    os.remove(file_path)
    del_photo.delete()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def friend_send(request, i):
    rec_user = get_object_or_404(User, pk=i)

    if Friends.objects.filter(friend_reciever=rec_user, friend_sender=request.user):
        get_object_or_404(Friends, friend_reciever=rec_user, friend_sender=request.user).delete()

    elif not Friends.objects.filter(friend_reciever = request.user, friend_sender = rec_user):
        Friends(friend_reciever = rec_user, friend_sender = request.user).save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def friend_requests(request):
    data={}
    data['requests'] = User.objects.filter(f_s__friend_reciever=request.user).all()
    data['friend_subscribe'] = Friends.objects.filter(friend_reciever=request.user).all()
    return render(request, 'friend_request_list.html', data)

@login_required
def friend_response(request, i):
    friend_response = get_object_or_404(Friends, friend_reciever=request.user, friend_sender_id=i)
    friend_response.subscribe=True
    friend_response.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def friend_reject(request, i):
    friend_response = get_object_or_404(Friends, friend_reciever=request.user, friend_sender_id=i)
    friend_response.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])