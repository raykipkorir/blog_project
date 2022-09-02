from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthBackend:

    def authenticate(self, request, username = None, password = None, *args, **kwargs):
        try:
            user = User.objects.get(email = username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self,id):
        try:
            user = User.objects.get(pk = id)
            return user
        except User.DoesNotExist:
            return None
            