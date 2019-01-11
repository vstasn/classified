from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Ads, AdsCity


class AdsAdminSite(AdminSite):
    """
    Admin management for Ads
    Without updating Cities, because just user that is_staff can add new city
    """

    site_header = "Ads administration"

    def has_permission(self, request):
        return request.user.is_active


class AdminModel(admin.ModelAdmin):

    using = "DATABASE_NAME"
    list_display = ("title", "description", "city", "owner")
    exclude = ["owner"]

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        """
        Filter object just view if user is owner of ads
        """
        qs = super(AdminModel, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(owner=request.user)

    def has_module_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser or obj.owner == request.user:
            return True
        else:
            return False

    def has_add_permission(self, request):
        return True

    def has_permission(self, request):
        """
        Possible to use admin also if user is not staff
        """
        return request.user.is_active

    has_delete_permission = has_change_permission


admin_site = AdsAdminSite(name="ads")
admin_site.register(Ads, AdminModel)

admin.site.register(Ads)
admin.site.register(AdsCity)
