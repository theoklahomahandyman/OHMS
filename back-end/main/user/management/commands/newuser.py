from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.core import exceptions
from user.models import User

class Command(BaseCommand):
    help = 'Used to create a new user following the project database guidelines.'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--first-name', type=str, help='Define a first name.')
        parser.add_argument('-l', '--last-name', type=str, help='Define a last name.')
        parser.add_argument('-e', '--email', type=str, help='Define an email.')
        parser.add_argument('-p', '--phone', type=str, help='Define a phone number.')

    def handle(self, *args, **kwargs):
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        email = kwargs['email']
        phone = kwargs['phone']

        first_name = self._validate_or_prompt_value(first_name, 'first name', User._meta.get_field('first_name').validators)
        last_name = self._validate_or_prompt_value(last_name, 'last name', User._meta.get_field('last_name').validators)
        email = self._validate_or_prompt_value(email, 'email', User._meta.get_field('email').validators)
        phone = self._validate_or_prompt_value(phone, 'phone', User._meta.get_field('phone').validators)

        try:
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, password=make_password('newuser123'))
            user.save()
            print(self.style.SUCCESS(f'User created successfully for user with email {user.email}. Please use the password "newuser123" to login and change your password.'))
        except exceptions.ValidationError as error:
            print(self.style.ERROR(f'Error creating user: {error}'))

    def _validate_or_prompt_value(self, value, field_name, validators):
        while not value:
            if field_name[0] in ['a', 'e', 'i', 'o']:
                value = input(f'Please enter an {field_name}: ').strip()
            else:
                value = input(f'Please enter a {field_name}: ').strip()
            for validator in validators:
                try:
                    validator(value)
                except exceptions.ValidationError as error:
                    print(self.style.ERROR(f'Invalid {field_name}: {error}'))
                    value = None
                    break
            if field_name in ('email'):
                try:
                    user = User.objects.get(email=value)
                except:
                    user = None
                if user is not None:
                    print(self.style.ERROR(f'A user with the {field_name} {value} already exists.'))
                    value = None
        return value
    