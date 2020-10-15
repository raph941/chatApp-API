from django.test import TestCase
from accounts.models import User
from django.contrib.auth import authenticate


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='user_pass', email="user@email.com", fullname="John Doe", image_url='')
        
    def test_user_properties(self):
        username = self.user.username
        email = self.user.email
        fullname = self.user.fullname
        imageUrl = self.user.image_url

        self.assertEqual(username, 'user')
        self.assertEqual(email, 'user@email.com')
        self.assertEqual(fullname, 'John Doe')
        self.assertEqual(imageUrl, '')