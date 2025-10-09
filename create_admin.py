#!/usr/bin/env python
"""
Script to create admin user for Strathmore Insight Nexus.
Run this after migrations: python create_admin.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authentication.settings')
django.setup()

from api.models import User
from django.contrib.auth.hashers import make_password


def create_admin_user():
    """Create or update admin user."""
    email = 'walter45oyugi@gmail.com'
    
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        print(f"⚠️  User {email} already exists!")
        user = User.objects.get(email=email)
        print(f"Current role: {user.role}")
        print(f"Email verified: {user.is_email_verified}")
        print(f"Is staff: {user.is_staff}")
        print(f"Is superuser: {user.is_superuser}")
        
        response = input("\nDo you want to update this user? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
        
        # Update existing user
        password = input("Enter new password (leave blank to keep current): ")
        if password:
            user.set_password(password)
        
        user.role = 'executive'
        user.is_email_verified = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        print(f"\n✅ Admin user updated successfully!")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        
    else:
        # Create new admin user
        print(f"Creating admin user: {email}")
        
        first_name = input("Enter first name (default: Walter): ") or "Walter"
        last_name = input("Enter last name (default: Oyugi): ") or "Oyugi"
        password = input("Enter password: ")
        
        if not password:
            print("❌ Password is required!")
            return
        
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='executive',
            is_email_verified=True,
            is_staff=True,
            is_superuser=True
        )
        
        print(f"\n✅ Admin user created successfully!")
        print(f"Email: {user.email}")
        print(f"Name: {user.first_name} {user.last_name}")
        print(f"Role: {user.role}")
        print(f"\n🔐 You can now login with these credentials!")


if __name__ == '__main__':
    print("=" * 60)
    print("🔐 Strathmore Insight Nexus - Admin User Setup")
    print("=" * 60)
    print()
    
    create_admin_user()
    
    print("\n" + "=" * 60)

