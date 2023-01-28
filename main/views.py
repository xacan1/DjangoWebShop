from django.views.generic import FormView, ListView, DetailView, CreateView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from main.models import *
from main.forms import *
from shop.mixins import DataMixin


class PageNotFound(FormView):
    form_class = SimpleForm
    template_name = 'main/page404.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response


class LoginUserView(DataMixin, auth_views.LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(auth_views.LogoutView):
    next_page = 'home'


class RegisterUserView(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('registration-success')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}


class RegisterUserSuccessView(DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'main/registration-success.html'


class VersaPasswordChangeView(DataMixin, auth_views.PasswordChangeView):
    form_class = VersaPasswordChangeForm
    template_name = 'main/password-change.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение пароля')
        return {**context, **c_def}


class VersaPasswordChangeDoneView(DataMixin, auth_views.PasswordChangeDoneView):
    template_name = 'main/password-change-done.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пароль успешно изменен!')
        return {**context, **c_def}


class VersaPasswordResetView(DataMixin, auth_views.PasswordResetView):
    form_class = VersaPasswordResetForm
    template_name = 'main/password-reset.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Сброс пароля')
        return {**context, **c_def}


class VersaPasswordResetConfirmView(DataMixin, auth_views.PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name = 'main/password-reset-confirm.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}


class VersaPasswordResetDoneView(DataMixin, auth_views.PasswordResetDoneView):
    template_name = 'main/password-reset-done.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Письмо с инструкциями по восстановлению пароля отправлено')
        return {**context, **c_def}


class VersaPasswordResetCompleteView(DataMixin, auth_views.PasswordResetCompleteView):
    template_name = 'main/password-reset-complete.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Восстановление пароля завершено')
        return {**context, **c_def}
