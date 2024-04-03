from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class BaseEmailSender:
    template_name = None
    subject = None
    user_id_field = "pk"

    def __init__(self, request, user: AbstractUser):
        self._request = request
        self._user = user

    def get_template_name(self) -> str:
        if self.template_name is None:
            raise NotImplemented("Вы должны указать имя шаблона в атрибуте класса")
        return self.template_name

    def get_subject(self) -> str:
        if self.subject is None:
            raise NotImplemented("Укажите тему письма в атрибуте класса")
        return self.subject

    def send_mail(self):
        mail = EmailMultiAlternatives(
            subject=self.get_subject() + " на сайте " + self._get_domain(),
            to=[self._user.email]
        )
        mail.attach_alternative(self._get_mail_body(), "text/html")
        mail.send()

    def _get_mail_body(self) -> str:
        context = {
            "user": self._user,
            "domain": self._get_domain(),
            "uidb64": self._get_user_base64(),
            "token": self._get_token(),
        }
        return render_to_string(self.get_template_name(), context)

    def _get_domain(self) -> str:
        return str(get_current_site(self._request))

    def _get_token(self) -> str:
        return default_token_generator.make_token(self._user)

    def _get_user_base64(self) -> str:
        """Кодируем идентификационное поле пользователя, указанное в атрибуте класса"""
        return urlsafe_base64_encode(
            force_bytes(str(getattr(self._user, self.user_id_field)))
        )





class ConfirmUserRegisterEmailSender(BaseEmailSender):
    template_name = "registration/email_confirm.html"
    user_id_field = "username"
    subject = "Подтвердите регистрацию"


class ConfirmUserResetPasswordEmailSender(BaseEmailSender):
    template_name = "password/password_reset_request.html"
    user_id_field = "username"
    subject = "Сброс пароля"
# ===================================================

class BaseEmailSender:
    def __init__(self, request, user: AbstractUser):
        self.request = request
        self.user = user

    def send_mail(self, template_name, subject, user_id_field="username"):
        context = {"user": self.user,
                   "domain": str(get_current_site(self.request)),
                   "uid64": urlsafe_base64_encode(force_bytes(str(getattr(self.user,user_id_field )))),
                   "token": default_token_generator.make_token(self.user),}
        mail_body = render_to_string(template_name, context)
        mail_subject = f"{subject} на сайте {context['domain']}"

        mail = EmailMultiAlternatives(subject=mail_subject, to=[self.user.email])
        mail.attach_alternative(mail_body, "text/html")
        mail.send()

# Использование класса
email_sender = BaseEmailSender(request, user)
email_sender.send_mail("registration/email_confirm.html", "Подтвердите регистрацию")
email_sender.send_mail("password/password_reset_request.html", "Сброс пароля")

# ===================================================