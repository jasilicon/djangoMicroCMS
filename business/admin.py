from django.contrib import admin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdminMixin
from micro_cms.admin import owner_admin_site
from .models import Business, HeroImage, SectionPublish, SiteSetting


class SectionPublishInline(admin.TabularInline):
    model = SectionPublish
    extra = 7
    max_num = 7


class HeroImageInline(admin.TabularInline):
    model = HeroImage
    extra = 1


class BusinessAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    summernote_fields = ("about",)
    list_display = ("name", "owner", "is_published", "updated_at")
    search_fields = ("name", "owner__username")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SectionPublishInline, HeroImageInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def get_fields(self, request, obj=None):
        fields = ["name", "tagline", "about", "address", "phone", "email", "google_maps_embed_url", "logo", "favicon"]
        if request.user.is_superuser:
            fields.append("is_published")
        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.owner_id:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.owner == request.user

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class SectionPublishAdmin(admin.ModelAdmin):
    list_display = ("business", "section_slug", "is_published")
    list_filter = ("section_slug", "is_published")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(business__owner=request.user)


class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("business", "key", "value")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(business__owner=request.user)


class HeroImageAdmin(admin.ModelAdmin):
    list_display = ("business", "alt_text", "is_published", "sort_order")
    list_editable = ("is_published", "sort_order")

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


admin.site.register(Business, BusinessAdmin)
admin.site.register(SectionPublish, SectionPublishAdmin)
admin.site.register(SiteSetting, SiteSettingAdmin)
admin.site.register(HeroImage, HeroImageAdmin)

owner_admin_site.register(Business, BusinessAdmin)
owner_admin_site.register(SectionPublish, SectionPublishAdmin)
owner_admin_site.register(SiteSetting, SiteSettingAdmin)
owner_admin_site.register(HeroImage, HeroImageAdmin)
