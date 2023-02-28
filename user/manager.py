from django.contrib.auth.models import BaseUserManager
from django_softdelete.models import DeletedManager, GlobalManager, SoftDeleteManager


class SoftDeleteUserManager(SoftDeleteManager, DeletedManager, GlobalManager):
    pass


class UserManager(BaseUserManager, SoftDeleteUserManager):

    def create_user(self, username, email, password=None, is_verified=False, is_active=True):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.is_employee = False
        user.is_verified = is_verified
        user.is_active = is_active
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user
