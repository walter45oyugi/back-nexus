from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

from .models import User, LoginAttempt
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    VerifyEmailSerializer, ChangePasswordSerializer,
    AdminCreateUserSerializer, LoginAttemptSerializer,
    RequestApprovalSerializer, ApproveUserSerializer
)
from .permissions import IsAdmin
from .utils import generate_verification_code, generate_admin_token, get_verification_code_expiry


def get_tokens_for_user(user):
    """Generate JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    
    # Add custom claims to the token
    refresh['email'] = user.email
    refresh['role'] = user.role
    
    # Set token expiration based on user role
    if user.email == settings.ADMIN_EMAIL:
        # Admin gets 1 year token
        refresh.set_exp(lifetime=timedelta(days=365))
    else:
        # Regular users get 20 minutes
        refresh.set_exp(lifetime=timedelta(minutes=20))
    
    return {
        'token': str(refresh.access_token),
        'refresh': str(refresh),
    }


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    POST /api/auth/register/
    Register a new user.
    """
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate verification code
        verification_code = generate_verification_code()
        user.verification_code = verification_code
        user.verification_code_expiry = get_verification_code_expiry()
        user.save()
        
        # TODO: Send verification email
        # For now, we'll just return the code in development
        # In production, send email via SendGrid/Mailgun
        
        return Response({
            'success': True,
            'message': 'User registered successfully. Please verify your email.',
            'user': UserSerializer(user).data,
            # Remove this in production - only for development
            'verification_code': verification_code if settings.DEBUG else None
        }, status=status.HTTP_201_CREATED)
    
    # Handle validation errors
    errors = []
    for field, messages in serializer.errors.items():
        if isinstance(messages, list):
            errors.append(f"{field}: {', '.join(messages)}")
        else:
            errors.append(f"{field}: {messages}")
    
    return Response({
        'success': False,
        'message': '; '.join(errors)
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """
    POST /api/auth/verify-email/
    Verify user email with code.
    """
    serializer = VerifyEmailSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Invalid data provided.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    code = serializer.validated_data['code']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if already verified
    if user.is_email_verified:
        return Response({
            'success': False,
            'message': 'Email is already verified.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if code matches
    if user.verification_code != code:
        return Response({
            'success': False,
            'message': 'Invalid verification code.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if code is expired
    if user.verification_code_expiry and user.verification_code_expiry < timezone.now():
        return Response({
            'success': False,
            'message': 'Verification code has expired. Please request a new one.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify the email
    user.is_email_verified = True
    user.verification_code = None
    user.verification_code_expiry = None
    user.save()
    
    return Response({
        'success': True,
        'message': 'Email verified successfully! You can now log in.'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    POST /api/auth/login/
    User login with email and password.
    """
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Invalid data provided.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    # Check if user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found. Please register first.'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if email is verified
    if not user.is_email_verified:
        return Response({
            'success': False,
            'message': 'Please verify your email before logging in.'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Get or create login attempt record
    login_attempt, created = LoginAttempt.objects.get_or_create(email=email)
    
    # Check if account is blocked
    if login_attempt.blocked and not login_attempt.admin_approved:
        return Response({
            'success': False,
            'message': 'Account is blocked due to too many failed login attempts. Please contact admin for approval.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Verify password
    if check_password(password, user.password):
        # Password is correct - reset login attempts
        login_attempt.attempts = 0
        login_attempt.blocked = False
        login_attempt.save()
        
        # Update last login time
        user.last_login_at = timezone.now()
        user.save()
        
        # Generate JWT token
        tokens = get_tokens_for_user(user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'token': tokens['token'],
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    else:
        # Password is incorrect - increment attempts
        login_attempt.attempts += 1
        remaining_attempts = 5 - login_attempt.attempts
        
        # Block if attempts >= 5
        if login_attempt.attempts >= 5:
            login_attempt.blocked = True
            login_attempt.save()
            return Response({
                'success': False,
                'message': 'Account is blocked due to too many failed login attempts. Please contact admin for approval.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        login_attempt.save()
        
        return Response({
            'success': False,
            'message': f'Invalid credentials. {remaining_attempts} attempts remaining.'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    GET /api/auth/me/
    Get current logged-in user info.
    """
    user = request.user
    return Response({
        'success': True,
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    POST /api/auth/logout/
    Logout user (token blacklisting).
    """
    try:
        # Get the refresh token from request
        refresh_token = request.data.get('refresh_token')
        
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'success': True,
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'success': True,
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    POST /api/auth/change-password/
    Change user password.
    """
    serializer = ChangePasswordSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Invalid data provided.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    current_password = serializer.validated_data['current_password']
    new_password = serializer.validated_data['new_password']
    
    # Check current password
    if not check_password(current_password, user.password):
        return Response({
            'success': False,
            'message': 'Current password is incorrect.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Set new password
    user.set_password(new_password)
    user.save()
    
    return Response({
        'success': True,
        'message': 'Password changed successfully!'
    }, status=status.HTTP_200_OK)


# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_all_users(request):
    """
    GET /api/admin/users/
    Get all users (Admin only).
    """
    users = User.objects.all()
    return Response({
        'success': True,
        'users': UserSerializer(users, many=True).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def admin_create_user(request):
    """
    POST /api/admin/create-user/
    Admin creates a new user (pre-verified).
    """
    serializer = AdminCreateUserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        return Response({
            'success': True,
            'message': 'User created successfully!',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    # Handle validation errors
    errors = []
    for field, messages in serializer.errors.items():
        if isinstance(messages, list):
            errors.append(f"{field}: {', '.join(messages)}")
        else:
            errors.append(f"{field}: {messages}")
    
    return Response({
        'success': False,
        'message': '; '.join(errors)
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def approve_user(request):
    """
    POST /api/admin/approve-user/
    Admin approves a blocked user.
    """
    serializer = ApproveUserSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Invalid data provided.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    admin_token = serializer.validated_data['admin_token']
    
    # Get login attempt record
    try:
        login_attempt = LoginAttempt.objects.get(email=email)
    except LoginAttempt.DoesNotExist:
        return Response({
            'success': False,
            'message': 'No login attempt record found for this email.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify admin token
    if login_attempt.admin_token != admin_token:
        return Response({
            'success': False,
            'message': 'Invalid admin token.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Approve the user
    login_attempt.admin_approved = True
    login_attempt.blocked = False
    login_attempt.attempts = 0
    login_attempt.admin_token = None
    login_attempt.save()
    
    return Response({
        'success': True,
        'message': 'User approved successfully.'
    }, status=status.HTTP_200_OK)


# ============================================================================
# LOGIN ATTEMPT ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_login_attempts(request, email):
    """
    GET /api/auth/login-attempts/<email>/
    Get login attempt info for an email.
    """
    try:
        login_attempt = LoginAttempt.objects.get(email=email)
        return Response({
            'success': True,
            'email': login_attempt.email,
            'attempts': login_attempt.attempts,
            'blocked': login_attempt.blocked,
            'admin_approved': login_attempt.admin_approved,
            'last_attempt': login_attempt.last_attempt
        }, status=status.HTTP_200_OK)
    
    except LoginAttempt.DoesNotExist:
        return Response({
            'success': True,
            'email': email,
            'attempts': 0,
            'blocked': False,
            'admin_approved': False,
            'last_attempt': None
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def setup_admin(request):
    """
    POST /api/admin/setup/
    One-time admin setup (only works if no admin exists).
    """
    # Check if admin already exists
    admin_exists = User.objects.filter(email=settings.ADMIN_EMAIL).exists()
    
    if admin_exists:
        return Response({
            'success': False,
            'message': 'Admin user already exists. This endpoint is disabled.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate setup key (simple security measure)
    setup_key = request.data.get('setup_key')
    if setup_key != 'STRATHMORE2024NEXUS':
        return Response({
            'success': False,
            'message': 'Invalid setup key.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    email = request.data.get('email', settings.ADMIN_EMAIL)
    password = request.data.get('password')
    first_name = request.data.get('first_name', 'Walter')
    last_name = request.data.get('last_name', 'Oyugi')
    
    if not password:
        return Response({
            'success': False,
            'message': 'Password is required.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create admin user
    admin_user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role='executive',
        is_email_verified=True,
        is_staff=True,
        is_superuser=True
    )
    
    return Response({
        'success': True,
        'message': 'Admin user created successfully! You can now login.',
        'user': UserSerializer(admin_user).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def request_admin_approval(request):
    """
    POST /api/auth/request-admin-approval/
    Request admin approval after being blocked.
    """
    serializer = RequestApprovalSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Invalid data provided.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    
    # Get login attempt record
    try:
        login_attempt = LoginAttempt.objects.get(email=email)
    except LoginAttempt.DoesNotExist:
        return Response({
            'success': False,
            'message': 'No login attempt record found for this email.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user has enough attempts to be blocked
    if login_attempt.attempts < 5:
        return Response({
            'success': False,
            'message': 'Account is not blocked.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate admin token
    admin_token = generate_admin_token()
    login_attempt.admin_token = admin_token
    login_attempt.save()
    
    # TODO: Send email to admin with token
    # For now, we'll just return the token in development
    
    return Response({
        'success': True,
        'message': 'Admin approval request sent. Please wait for approval.',
        'admin_token': admin_token if settings.DEBUG else None
    }, status=status.HTTP_200_OK)

