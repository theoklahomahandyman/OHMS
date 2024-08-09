from django.contrib.auth.hashers import make_password
from django.test import TestCase
from user.models import User

# Tests for user model
class TestUserModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.password = 'test1234'
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))

    ## Test string method for user model
    def test_user_string(self):
        self.assertEqual(str(self.user), f'{self.user.first_name} {self.user.last_name}')