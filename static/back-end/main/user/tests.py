from django.contrib.auth.hashers import make_password
from user.serializers import UserSerializer
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

# Tests for user serializer
class TestUserSerializer(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.password = 'test1234'
        cls.update_password = 'new12345'
        cls.long_string = 'a' * 256
        cls.user = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
        cls.empty_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone': '',
            'password': '',
            'confirm_password': '',
        }
        cls.short_data = {
            'first_name': 'J',
            'last_name': 'D',
            'email': 'j@e.com',
            'phone': '183043',
            'password': 'test',
            'confirm_password': 'test',
        }
        cls.long_data = {
            'first_name': cls.long_string,
            'last_name': cls.long_string,
            'email': cls.long_string + '@example.com',
            'phone': cls.long_string,
            'password': cls.password,
            'confirm_password': cls.password,
        }
        cls.create_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '1 (586) 375-3896',
            'password': cls.password,
            'confirm_password': cls.password,
        }
        cls.update_data = {
            'first_name': 'Bill',
            'last_name': 'Johnson',
            'email': 'billjohnson@example.com',
            'phone': '45 (192) 937-9329',
            'password': cls.update_password,
            'confirm_password': cls.update_password,
        }

    ## Test validate with empty data
    def test_validate_empty_data(self):
        serializer = UserSerializer(data=self.empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)
        self.assertIn('last_name', serializer.errors)
        self.assertIn('email', serializer.errors)
        self.assertIn('phone', serializer.errors)
        self.assertIn('password', serializer.errors)
        self.assertIn('confirm_password', serializer.errors)
    
    ## Test validate with data too short
    def test_validate_short_data(self):
        serializer = UserSerializer(data=self.short_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)
        self.assertIn('last_name', serializer.errors)
        self.assertIn('email', serializer.errors)
        self.assertIn('phone', serializer.errors)

    ## Test validate with short password
    def test_validate_short_password(self):
        self.create_data['password'] = self.short_data['password']
        self.create_data['confirm_password'] = self.short_data['confirm_password']
        serializer = UserSerializer(data=self.create_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        
    ## Test validate with data too long
    def test_validate_long_data(self):
        serializer = UserSerializer(data=self.long_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)
        self.assertIn('last_name', serializer.errors)
        self.assertIn('email', serializer.errors)
        self.assertIn('phone', serializer.errors)
        
    ## Test validate with mismatching passwords
    def test_validate_mismatching_passwords(self):
        self.create_data['confirm_password'] = 'differentpassword'
        serializer = UserSerializer(data=self.create_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('confirm_password', serializer.errors)
        
    ## Test validate with invalid password
    def test_validate_invalid_password(self):
        self.create_data['password'] = self.create_data['first_name'] + self.create_data['last_name']
        self.create_data['confirm_password'] = self.create_data['first_name'] + self.create_data['last_name']
        serializer = UserSerializer(data=self.create_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    ## Test create success
    def test_create_success(self):
        serializer = UserSerializer(data=self.create_data)
        self.assertTrue(serializer.is_valid())
        user: User = serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(user.first_name, self.create_data['first_name'])
        self.assertEqual(user.last_name, self.create_data['last_name'])
        self.assertEqual(user.email, self.create_data['email'])
        self.assertEqual(user.phone, self.create_data['phone'])
        self.assertTrue(user.check_password(self.password))
                
    ## Test update success
    def test_update_success(self):
        serializer = UserSerializer(instance=self.user, data=self.update_data)
        self.assertTrue(serializer.is_valid())
        user: User = serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(user.first_name, self.update_data['first_name'])
        self.assertEqual(user.last_name, self.update_data['last_name'])
        self.assertEqual(user.email, self.update_data['email'])
        self.assertEqual(user.phone, self.update_data['phone'])
        self.assertTrue(user.check_password(self.update_password))
    