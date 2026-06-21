from django.contrib import admin
from micro_cms.admin import owner_admin_site
from .models import GalleryImage


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("caption", "business", "is_published", "sort_order")
    list_editable = ("sort_order", "is_published")

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


admin.site.register(GalleryImage, GalleryImageAdmin)
owner_admin_site.register(GalleryImage, GalleryImageAdmin)
