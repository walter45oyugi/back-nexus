from rest_framework import serializers
from .models import User, LoginAttempt


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'role',
            'is_email_verified', 'date_joined', 'last_login_at'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'role']
    
    def validate_email(self, value):
        """Check if email already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value
    
    def validate_password(self, value):
        """Validate password length."""
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value
    
    def create(self, validated_data):
        """Create a new user with hashed password."""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', 'maintenance')
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class VerifyEmailSerializer(serializers.Serializer):
    """Serializer for email verification."""
    
    email = serializers.EmailField()
    code = serializers.CharField(max_length=10)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
    
    def validate_new_password(self, value):
        """Validate new password length."""
        if len(value) < 6:
            raise serializers.ValidationError("New password must be at least 6 characters long.")
        return value


class AdminCreateUserSerializer(serializers.ModelSerializer):
    """Serializer for admin creating a new user."""
    
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'role']
    
    def validate_email(self, value):
        """Check if email already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value
    
    def create(self, validated_data):
        """Create a new user with email pre-verified."""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', 'maintenance'),
            is_email_verified=True  # Admin-created users are pre-verified
        )
        return user


class LoginAttemptSerializer(serializers.ModelSerializer):
    """Serializer for LoginAttempt model."""
    
    class Meta:
        model = LoginAttempt
        fields = ['email', 'attempts', 'blocked', 'admin_approved', 'last_attempt']
        read_only_fields = ['last_attempt']


class RequestApprovalSerializer(serializers.Serializer):
    """Serializer for requesting admin approval."""
    
    email = serializers.EmailField()


class ApproveUserSerializer(serializers.Serializer):
    """Serializer for admin approving a blocked user."""
    
    email = serializers.EmailField()
    admin_token = serializers.CharField(max_length=100)

