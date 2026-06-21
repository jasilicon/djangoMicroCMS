from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin


class OwnerAdminSite(AdminSite):
    site_header = "Micro-CMS Administration"
    site_title = "Micro-CMS Admin"
    index_title = "Dashboard"

    def has_permission(self, request):
        return request.user.is_active and (
            request.user.is_superuser or hasattr(request.user, "business")
        )


owner_admin_site = OwnerAdminSite(name="owner_admin")
owner_admin_site.register(Group, BaseGroupAdmin)
