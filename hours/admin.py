from django.contrib import admin
from micro_cms.admin import owner_admin_site
from .models import BusinessHour


class BusinessHourAdmin(admin.ModelAdmin):
    list_display = ("business", "day", "is_closed", "open_time", "close_time")
    list_editable = ("is_closed", "open_time", "close_time")

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


admin.site.register(BusinessHour, BusinessHourAdmin)
owner_admin_site.register(BusinessHour, BusinessHourAdmin)
