from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupAdminForm
from .models import (
    CustomUser,
    UserPassword,
    AgentInfo,
    Profile,
    AgentDocument,
    AgentLicense
)


admin.site.site_header = 'Bascule Admin Dashboard'
admin.site.unregister(Group)
admin.site.register(UserPassword)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('User Information', {'fields': ('email', 'password', 'first_name', 'last_name',)}),
        ('User Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'is_approve','user_permissions')}),
        ('User Type', {'fields': ('account_type',)}),
        ('Send email', {'fields': ('activation_email',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    model = Permission


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']
admin.site.register(Group, GroupAdmin)


@admin.register(AgentInfo)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['user','agency_name','agency_address','commission','type','uploaded','date']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','verified_equine','verified_farm']


@admin.register(AgentDocument)
class AgentDocumentAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','document']


@admin.register(AgentLicense)
class AgentLicenseAdmin(admin.ModelAdmin):
    list_display = ['id','user','state','document']
