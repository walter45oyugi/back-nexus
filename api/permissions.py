from rest_framework import permissions
from django.conf import settings


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    Admin is defined as the user with email matching ADMIN_EMAIL in settings.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user email matches admin email
        return request.user.email == settings.ADMIN_EMAIL

