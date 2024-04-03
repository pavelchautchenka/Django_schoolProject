from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from app.models import User
from django.http import HttpResponse
#12345678Az

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) +
                text_type(user.is_active))

account_activation_token = AccountActivationTokenGenerator()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    subject = 'Активация вашего аккаунта'
    message = render_to_string('user/email_confirm.html', {
        'user': user,
        'domain': current_site.domain,
        'uid64': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        user.save()

        return HttpResponse('Аккаунт активирован успешно!')
    else:
        return HttpResponse('Ссылка активации недействительна!')