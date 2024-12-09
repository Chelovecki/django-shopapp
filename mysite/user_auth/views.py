from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from shopapp.models import Product

from .models import Profile


class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        welcome_message = _("welcomee bro: Hello World")
        return HttpResponse(f"<h1>{welcome_message}</h1>")


class LoginPkView(LoginView):
    def form_valid(self, form):
        # Выполняем вход пользователя
        login(self.request, form.get_user())

        # Получаем pk авторизованного пользователя
        user_pk = form.get_user().pk

        # Перенаправляем на страницу с pk пользователя
        return redirect('user_auth:user_info', pk=user_pk)


class CreateUserView(CreateView):
    template_name = 'user_auth/user_create_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('user_auth:user_info')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        user = authenticate(
            self.request,
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password1')
        )
        login(self.request, user)

        return response


class ShowUserInfoView(TemplateView):
    template_name = 'user_auth/user_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.filter(created_by_id=self.request.user.pk)
        context['products'] = products

        user_pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_pk)
        context['user'] = user

        """
        Этот код корректен. Он берет первых 100 пользователей из базы данных. 
        Django использует ленивую загрузку, поэтому в переменную _100_users не будет загружено 1 миллион пользователей, 
        а только те записи, которые вам нужны.
        """
        _100_users = User.objects.all().order_by('username')[:100]
        context['users'] = _100_users

        can_update_info = self.request.user == user or self.request.user.is_superuser
        context['can_update_info'] = can_update_info

        return context


class UpdateUserView(UserPassesTestMixin, UpdateView):
    model = User
    fields = 'last_name', 'email'
    template_name = 'user_auth/user_update_form.html'

    def test_func(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return self.request.user == user or self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponse('<h1>Лол, ты не можешь менять данные других пользователей</h1>')

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        return user

    def get_success_url(self):
        return reverse('user_auth:user_info', kwargs=self.kwargs)

    def form_valid(self, form):
        # Сначала сохраняем изменения в User
        user = form.save()

        # Обновляем поле last_name в Profile
        profile = user.profile  # Получаем профиль текущего пользователя
        profile.last_name = user.last_name  # Обновляем last_name в Profile
        profile.save()  # Сохраняем изменения в Profile

        return super().form_valid(form)  # Возвращаем результат вызова родительского метода


class CreateProfileView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = 'first_name', 'middle_name', 'last_name', 'number', 'bio', 'avatar',
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs.get('pk'))
        form.instance.pk = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_auth:user_info', kwargs={'pk': self.kwargs.get('pk')})


class UpdateProfileView(UserPassesTestMixin, UpdateView):
    model = Profile
    fields = 'last_name', 'first_name', 'middle_name', 'number', 'bio', 'agree_save_data', 'avatar'
    template_name = 'user_auth/profile_update_form.html'

    # для проверки прав доступа - либо сам пользователь, либо суперюзер
    def test_func(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        print(user)
        return self.request.user == user or self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponse('<h1>Лол, ты не можешь менять данные других пользователей</h1>')

    def get_object(self, queryset=None):
        profile = Profile.objects.get(pk=self.kwargs.get('pk'))
        return profile

    def get_success_url(self):
        return reverse('user_auth:user_info', kwargs=self.kwargs)

    def form_valid(self, form):
        # Сначала сохраняем изменения в User
        profile = form.save()

        # Обновляем поле last_name в Profile
        user = profile.user  # Получаем профиль текущего пользователя
        user.last_name = profile.last_name  # Обновляем last_name в Profile
        user.save()  # Сохраняем изменения в Profile

        return super().form_valid(form)  # Возвращаем результат вызова родительского метода


# good pass is fgb97345wo3pg5ruh

def redirect_for_logged_user(request:HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(reverse('user_auth:user_info', kwargs={'pk':request.user.pk}))
    else:
        return redirect(reverse('user_auth:login'))

