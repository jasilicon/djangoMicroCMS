from django.contrib import admin
from micro_cms.admin import owner_admin_site
from .models import SocialLink


class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "label", "url", "business", "is_published")
    list_editable = ("is_published",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(business__owner=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.business.owner == request.user

    def save_model(self, request, obj, form, change):
        if not obj.pk and not request.user.is_superuser:
            obj.business = request.user.business
        super().save_model(request, obj, form, change)


admin.site.register(SocialLink, SocialLinkAdmin)
owner_admin_site.register(SocialLink, SocialLinkAdmin)
