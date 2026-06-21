from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from micro_cms.admin import owner_admin_site


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "is_staff", "is_superuser")
    search_fields = ("username", "email")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
owner_admin_site.register(User, UserAdmin)
