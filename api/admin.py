from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LoginAttempt


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_email_verified', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_email_verified', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Verification', {'fields': ('is_email_verified', 'verification_code', 'verification_code_expiry')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'last_login_at', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'is_email_verified'),
        }),
    )


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """Admin configuration for LoginAttempt model."""
    
    list_display = ['email', 'attempts', 'blocked', 'admin_approved', 'last_attempt']
    list_filter = ['blocked', 'admin_approved']
    search_fields = ['email']
    ordering = ['-last_attempt']
    
    fieldsets = (
        (None, {'fields': ('email', 'attempts', 'last_attempt')}),
        ('Status', {'fields': ('blocked', 'admin_approved', 'admin_token')}),
    )
    
    readonly_fields = ['last_attempt']

