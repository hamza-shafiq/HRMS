from django.db.models import Manager, QuerySet


class TenantQuerySetMixin:
    tenant_fields = None

    def for_tenant(self, tenant):
        kwargs = {tenant_field: tenant for tenant_field in self.tenant_fields}
        return self.filter(**kwargs)

    def for_user(self, user, tenant):
        if not user.is_superuser:
            return self.for_tenant(tenant)

        return self


class BaseTenantQuerySet(TenantQuerySetMixin, QuerySet):
    tenant_fields = ['tenant']