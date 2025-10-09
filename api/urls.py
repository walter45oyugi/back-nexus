from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Authentication endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/verify-email/', views.verify_email, name='verify-email'),
    path('auth/login/', views.login, name='login'),
    path('auth/me/', views.get_current_user, name='me'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/change-password/', views.change_password, name='change-password'),
    
    # Admin endpoints
    path('admin/setup/', views.setup_admin, name='admin-setup'),  # One-time admin creation
    path('admin/users/', views.get_all_users, name='admin-users'),
    path('admin/create-user/', views.admin_create_user, name='admin-create-user'),
    path('admin/approve-user/', views.approve_user, name='approve-user'),
    
    # Login attempt endpoints
    path('auth/login-attempts/<str:email>/', views.get_login_attempts, name='login-attempts'),
    path('auth/request-admin-approval/', views.request_admin_approval, name='request-approval'),
]

