from django.contrib import admin
from micro_cms.admin import owner_admin_site
from .models import ServiceCategory, Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "is_published")
    inlines = [ServiceInline]

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


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "duration_minutes", "is_published")
    list_filter = ("category", "is_published")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(category__business__owner=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.category.business.owner == request.user

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category" and not request.user.is_superuser:
            kwargs["queryset"] = ServiceCategory.objects.filter(business__owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Service, ServiceAdmin)
owner_admin_site.register(ServiceCategory, ServiceCategoryAdmin)
owner_admin_site.register(Service, ServiceAdmin)
