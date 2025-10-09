import random
import string
from datetime import datetime, timedelta
from django.utils import timezone


def generate_verification_code(length=6):
    """Generate a random verification code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_admin_token():
    """Generate a unique admin token for approval requests."""
    timestamp = int(datetime.now().timestamp())
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"admin_{timestamp}_{random_string}"


def get_verification_code_expiry(minutes=15):
    """Get expiry time for verification code."""
    return timezone.now() + timedelta(minutes=minutes)

