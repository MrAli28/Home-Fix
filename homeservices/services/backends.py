from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentication backend which allows users to authenticate using either their
    username or email address
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find a user matching the username/email
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # No user was found matching the username/email
            return None
        except User.MultipleObjectsReturned:
            # More than one user has the same email (this shouldn't happen if email is unique)
            # In this case, we can return the first match
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
            if user.check_password(password):
                return user
            return None
