import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_softdelete.models import SoftDeleteModel
from rest_framework_simplejwt.tokens import RefreshToken

from .manager import UserBaseManager, UserManager, TenantQuerySet


class BaseModel(TimeStampedModel, SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    config = models.JSONField(blank=True, default=dict)

    class Meta:
        abstract = True


class Tenant(BaseModel):
    name = models.CharField(max_length=120)
    config = models.JSONField(default=dict, blank=True)

    objects = TenantQuerySet.as_manager()

    def __str__(self):
        return f'{self.name}'


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name='tenant_users')
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    all_objects = UserBaseManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        refresh['tenant_id'] = str(self.tenant.id) if self.tenant else None
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def reactivate_user(self, password=None):
        if password:
            self.password = password
        self.is_deleted = False
        self.save()
