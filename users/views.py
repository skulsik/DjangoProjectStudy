from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetDoneView, PasswordContextMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, CreateView, FormView
from pip._internal.utils._jaraco_text import _
from catalog.modules.services.utils import generation_password
from config import settings
from users.forms import UserForm, UserRegisterForm
from users.models import User


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:confirm_email')

    def form_valid(self, form):
        """ Дружественное письмо на почту пользователя, после регистрации """
        new_user = form.save()
        user_pk = new_user.pk
        new_token = token_generator.make_token(new_user)
        send_mail(
            subject='ConstructionStore',
            message=f'Убедительная просьба: если хотите закончить регистрацию, пройдите по ссылке: http://127.0.0.1:8000/users/verify_email/{ urlsafe_base64_encode(force_bytes(user_pk)) }/{ new_token }',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserPasswordResetView(PasswordContextMixin, FormView):
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:password_reset_done")
    title = _("Password reset")
    template_name = 'users/password_reset_form.html'

    def form_valid(self, form):
        """ Дружественное письмо на почту пользователя, после регистрации """
        user_email: str = self.request.POST.get('email')
        new_password: str = generation_password()
        user_object: object = User.objects.get(email=user_email)
        send_mail(
            subject='ConstructionStore - Восстановление пароля',
            message=f'Вас приветствует администрация ConstructionStore.\nВы запросили новый пароль для {user_email}.\nВаш новый пароль: {new_password}\nС уважением администрация ConstructionStore.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email]
        )
        user_object.set_password(new_password)
        user_object.save()
        return super().form_valid(form)


class UserPasswordResetDoneView(PasswordResetDoneView):
    PasswordResetDoneView.template_name = 'users/password_reset_done.html'


class UserActivate(View):
    def get(self, request, uidb64, token):
        #user = self.get_user(uidb64)
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            print('user activate')
            return redirect('users:login')
        return redirect('users:invalid_user_activate')


    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


class InvalidUserActivate(View):
    template_name = 'users/invalid_user_activate.html'
