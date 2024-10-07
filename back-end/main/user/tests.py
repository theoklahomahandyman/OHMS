from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from user.serializers import UserSerializer
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
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
            'pay_rate': ''
        }
        cls.short_data = {
            'first_name': 'J',
            'last_name': 'D',
            'email': 'j@e.com',
            'phone': '183043',
            'password': 'test',
            'confirm_password': 'test',
            'pay_rate': 12.34
        }
        cls.long_data = {
            'first_name': cls.long_string,
            'last_name': cls.long_string,
            'email': cls.long_string + '@example.com',
            'phone': cls.long_string,
            'password': cls.password,
            'confirm_password': cls.password,
            'pay_rate': 22449234872348438728399239238329390
        }
        cls.create_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '1 (586) 375-3896',
            'password': cls.password,
            'confirm_password': cls.password,
            'pay_rate': 12.34
        }
        cls.update_data = {
            'first_name': 'Bill',
            'last_name': 'Johnson',
            'email': 'billjohnson@example.com',
            'phone': '45 (192) 937-9329',
            'password': cls.update_password,
            'confirm_password': cls.update_password,
            'pay_rate': 18.35
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
        user.refresh_from_db()
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
        user.refresh_from_db()
        self.assertEqual(user.first_name, self.update_data['first_name'])
        self.assertEqual(user.last_name, self.update_data['last_name'])
        self.assertEqual(user.email, self.update_data['email'])
        self.assertEqual(user.phone, self.update_data['phone'])
        self.assertTrue(user.check_password(self.update_password))

# Tests for user view
class TestUserView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user_url = reverse('user')
        cls.admin_list_url = reverse('admin-list')
        cls.admin_detail_url = lambda pk: reverse('admin-detail', kwargs={'pk': pk})
        cls.long_string = 'a' * 256
        cls.password = 'test1234'
        cls.update_password = 'newuser1'
        cls.updated_first_name = 'Yuri'
        cls.user1 = User.objects.create(first_name='first', last_name='last', email='firstlast@example.com', phone='1 (234) 567-8901', password=make_password(cls.password))
        cls.user2 = User.objects.create(first_name='other', last_name='usser', email='otheruser@example.com', phone='3 (987) 502-1005', password=make_password(cls.password))
        cls.patch_data = {
            'password': cls.update_password,
            'confirm_password': cls.update_password,
        }
        cls.empty_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone': '',
            'password': '',
            'confirm_password': '',
            'is_active': True,
            'pay_rate': ''
        }
        cls.short_data = {
            'first_name': 'J',
            'last_name': 'D',
            'email': 'j@e.com',
            'phone': '183043',
            'password': 'test',
            'confirm_password': 'test',
            'is_active': True,
            'pay_rate': 15.23
        }
        cls.long_data = {
            'first_name': cls.long_string,
            'last_name': cls.long_string,
            'email': cls.long_string + '@example.com',
            'phone': cls.long_string,
            'password': cls.password,
            'confirm_password': cls.password,
            'is_active': True,
            'pay_rate': 12354351354646513684313548634638183483138
        }
        cls.create_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '1 (586) 375-3896',
            'is_active': True,
            'pay_rate': 15.25
        }
        cls.update_data = {
            'first_name': 'Bill',
            'last_name': 'Johnson',
            'email': 'billjohnson@example.com',
            'phone': '45 (192) 937-9329',
            'password': cls.update_password,
            'confirm_password': cls.update_password,
            'is_active': True,
            'pay_rate': 19.35
        }

    ## Test get user success
    def test_get_user_success(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user2.first_name)
        self.assertEqual(response.data['last_name'], self.user2.last_name)
        self.assertEqual(response.data['email'], self.user2.email)
        self.assertEqual(response.data['phone'], self.user2.phone)
        self.assertEqual(response.data['is_active'], self.user2.is_active)

    ## Test get user admin not found
    def test_get_user_admin_not_found(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.admin_detail_url(1215868))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Administrator Not Found.')

    ## Test get user admin success
    def test_get_user_admin_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.admin_detail_url(self.user2.pk))
        self.assertEqual(response.data['first_name'], self.user2.first_name)
        self.assertEqual(response.data['last_name'], self.user2.last_name)
        self.assertEqual(response.data['email'], self.user2.email)
        self.assertEqual(response.data['phone'], self.user2.phone)
        self.assertEqual(response.data['is_active'], self.user2.is_active)

    ## Test get users admin success
    def test_get_users_admin_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.admin_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.count())

    ## Test create user with empty data
    def test_create_user_empty_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.admin_list_url, self.empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    ## Test create user with short data
    def test_create_user_short_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.admin_list_url, self.short_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('phone', response.data)

    ## Test create user with existing email
    def test_create_user_existing_email(self):
        self.client.force_authenticate(user=self.user1)
        self.create_data['email'] = self.user2.email
        response = self.client.post(self.admin_list_url, self.create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    ## Test create user success
    def test_create_user_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.admin_list_url, self.create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    ## Test update user admin with empty data
    def test_update_user_admin_empty_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.admin_detail_url(self.user2.pk), {'first_name': self.empty_data['first_name']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

    ## Test update user admin with short data
    def test_update_user_admin_short_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.admin_detail_url(self.user2.pk), {'first_name': self.short_data['first_name']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

    ## Test update user admin with long data
    def test_update_user_admin_long_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.admin_detail_url(self.user2.pk), {'first_name': self.long_data['first_name']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

    ## Test update user admin with valid data
    def test_update_user_admin_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.admin_detail_url(self.user2.pk), {'first_name': self.updated_first_name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.first_name, self.updated_first_name)

    ## Test update user with empty data
    def test_update_user_empty_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.user_url, {'first_name': self.empty_data['first_name']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

    ## Test update user with short data
    def test_update_user_short_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.user_url, {'first_name': self.short_data['first_name']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

    ## Test update user with long data
    def test_update_user_long_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.user_url, {'first_name': self.long_data['first_name']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

    ## Test update user with valid data
    def test_update_user_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.user_url, {'first_name': self.updated_first_name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, self.updated_first_name)

    ## Test update user with short password
    def test_update_user_short_password(self):
        self.client.force_authenticate(user=self.user1)
        self.patch_data['password'] = self.short_data['password']
        self.patch_data['confirm_password'] = self.short_data['confirm_password']
        response = self.client.patch(self.user_url, self.patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    ## Test update user with mismatching passwords
    def test_update_user_mismatching_passwords(self):
        self.client.force_authenticate(user=self.user1)
        self.patch_data['confirm_password'] = 'mismatchingpasswords'
        response = self.client.patch(self.user_url, self.patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data)

    ## Test update user with invalid password
    def test_update_user_invalid_passwords(self):
        self.client.force_authenticate(user=self.user1)
        self.patch_data['password'] = self.user1.first_name + self.user1.last_name
        self.patch_data['confirm_password'] = self.user1.first_name + self.user1.last_name
        response = self.client.patch(self.user_url, self.patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    ## Test update user password success
    def test_update_user_password_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.user_url, self.patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.check_password(self.update_password))

    ## Test delete user success
    def test_delete_user_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.admin_detail_url(self.user2.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
