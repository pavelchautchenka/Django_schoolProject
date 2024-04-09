import datetime
from django.utils.deprecation import MiddlewareMixin


class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request,'user'):
            username = request.user.username if request.user.is_authenticated else 'Anonymous'
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log = f'{time}|{username}|URL={request.get_full_path()}\n'
            with open("userActivity.log", 'a', encoding="utf-8") as log_file:
                log_file.write(log)
