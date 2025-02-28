#!/usr/bin/env python
import os
import sys
import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

# Add the bots/src directory to the Python path
sys.path.append('/app/bots/src')

# Initialize Django if running standalone
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bots.config.settings")
    import django
    django.setup()

class AuthenticationTestCase(TestCase):
    """Test suite for the authentication system."""
    
    def setUp(self):
        """Set up test data before each test."""
        # Create a test user
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**self.credentials)
        
        # Create a test admin user
        self.admin_credentials = {
            'username': 'admin_test',
            'password': 'admin_password'
        }
        self.admin_user = User.objects.create_user(
            **self.admin_credentials,
            is_staff=True,
            is_superuser=True
        )
        
        # Create a test client
        self.client = Client()
        
        # Log test setup
        print(f"Test users created: {self.user.username}, {self.admin_user.username}")
    
    def test_login_url_exists(self):
        """Test that the login URL is accessible."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        print(f"Login URL test: status={response.status_code}")
    
    def test_login_form_contains_csrf(self):
        """Test that the login form contains a CSRF token."""
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        print("CSRF token test: Found in login form")
    
    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        
        # Print detailed debug information
        print(f"Login response status: {response.status_code}")
        print(f"Login response redirect chain: {response.redirect_chain}")
        print(f"Login session keys: {list(self.client.session.keys())}")
        
        # Check that the user is authenticated
        self.assertTrue(response.context['user'].is_authenticated)
        
        # Check redirect to home page
        self.assertRedirects(response, reverse('home'))
    
    def test_login_failure(self):
        """Test login with invalid credentials."""
        response = self.client.post(
            reverse('login'), 
            {'username': 'wrong', 'password': 'wrong'}, 
            follow=True
        )
        
        # Print debug information
        print(f"Failed login response status: {response.status_code}")
        
        # Check that the user is not authenticated
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_logout(self):
        """Test logout functionality."""
        # First login
        self.client.login(**self.credentials)
        
        # Then logout
        response = self.client.get(reverse('logout'), follow=True)
        
        # Print debug information
        print(f"Logout response status: {response.status_code}")
        print(f"Logout response redirect chain: {response.redirect_chain}")
        
        # Check that the user is logged out
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_login_required_views(self):
        """Test that protected views require login."""
        # Try to access a protected view
        response = self.client.get(reverse('home'), follow=True)
        
        # Should redirect to login
        self.assertRedirects(
            response, 
            f"{reverse('login')}?next={reverse('home')}"
        )
        
        # Now login and try again
        self.client.login(**self.credentials)
        response = self.client.get(reverse('home'))
        
        # Should be accessible now
        self.assertEqual(response.status_code, 200)
        print(f"Protected view test: status before login={response.status_code}")
    
    def test_admin_access(self):
        """Test that admin interface requires admin privileges."""
        # Regular user should not access admin
        self.client.login(**self.credentials)
        response = self.client.get('/admin/', follow=True)
        
        # Print debug information
        print(f"Admin access (regular user) response status: {response.status_code}")
        
        # Regular user should be redirected or get forbidden
        self.assertNotEqual(response.status_code, 200)
        
        # Admin user should access admin
        self.client.logout()
        self.client.login(**self.admin_credentials)
        response = self.client.get('/admin/')
        
        # Print debug information
        print(f"Admin access (admin user) response status: {response.status_code}")
        
        # Admin user should get access
        self.assertEqual(response.status_code, 200)
    
    def test_session_persistence(self):
        """Test that session persists across requests."""
        # Login
        self.client.login(**self.credentials)
        
        # Set a session variable
        session = self.client.session
        session['test_key'] = 'test_value'
        session.save()
        
        # Make another request
        response = self.client.get(reverse('home'))
        
        # Check that session variable is still there
        self.assertEqual(self.client.session['test_key'], 'test_value')
        print("Session persistence test: session variable persisted")
    
    def test_login_redirect_authenticated_user(self):
        """Test that authenticated users are redirected when visiting login page."""
        # Login
        self.client.login(**self.credentials)
        
        # Try to access login page
        response = self.client.get(reverse('login'), follow=True)
        
        # Should redirect to home page
        self.assertRedirects(response, reverse('home'))
        print(f"Login redirect test: {response.redirect_chain}")

if __name__ == '__main__':
    unittest.main() 