from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class DashboardTests(TestCase):

    def test_homepage_loads_successfully(self):
        """Sprawdza, czy strona główna zwraca 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        """Sprawdza, czy strona rejestracji działa poprawnie."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        """Testuje, czy formularz rejestracji tworzy użytkownika."""
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
        self.assertEqual(response.status_code, 302)  # powinno przekierować
        self.assertTrue(User.objects.filter(username='testuser').exists())
