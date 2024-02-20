from django.contrib.auth.backends import BaseBackend

from .models import Client


class AccountBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Client.objects.get(username=username)
        except Client.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None
