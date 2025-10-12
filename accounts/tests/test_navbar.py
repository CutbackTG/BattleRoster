from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class NavbarAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_navbar_shows_login_when_logged_out(self):
        """Navbar should show 'Sign-up / Log-in' when user is not logged in."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Sign-up / Log-in')
        self.assertNotContains(response, 'Log out')

    def test_navbar_shows_logout_when_logged_in(self):
        """Navbar should show 'Log out' when user is logged in."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Log out')
        self.assertNotContains(response, 'Sign-up / Log-in')

# run this with python manage.py test accounts
