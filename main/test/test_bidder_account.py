from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .factory import UserFactory
from faker import Faker
from ..models import CustomUser


class BidderSignUpTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_object = UserFactory.build()
        cls.user_saved = UserFactory.create()
        cls.client = APIClient()
        cls.signup_url = reverse('register')
        cls.faker_obj = Faker()

    def test_if_data_is_correct_then_signup(self):
        # Prepare data
        signup_dict = {
            'email': self.user_object.email,
            'password': '12345',
            'password_confirm': '12345',
        }
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(CustomUser.objects.count(), 2)
        # Check database
        new_user = CustomUser.objects.get(email=self.user_object.email)
        self.assertEqual(
            new_user.email,
            self.user_object.email,
        )

    def test_if_email_already_exists_dont_signup(self):
        # Prepare data with already saved user
        signup_dict = {
            'email': self.user_saved.email,
            'password': '12345',
            'password_confirm': '12345',
        }
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['email'][0]),
            'user with this email already exists.',
        )
        # Check database
        # Check that there is only one user with the saved email
        email_query = CustomUser.objects.filter(email=self.user_saved.email)
        self.assertEqual(email_query.count(), 1)


class BidderLogInTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_object = UserFactory.build()
        cls.user_saved = UserFactory.create()
        cls.client = APIClient()
        cls.signup_url = reverse('login')
        cls.login_url = reverse('login')
        cls.faker_obj = Faker()

    def test_if_data_is_correct_then_login(self):
        # Prepare data
        login_dict = {
            'email': self.user_object.email,
            'password': '12345',
        }
        # Create User
        CustomUser.objects.create_user(
            login_dict['email'], login_dict['password'])
        response = self.client.post(self.login_url, login_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_password_is_incorrect_then_dont_login(self):
        # Prepare data
        login_dict = {
            'email': self.user_object.email,
            'password': '',
        }
        # Create User
        CustomUser.objects.create_user(login_dict['email'], '12345')
        response = self.client.post(self.login_url, login_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data['detail']),
            'Incorrect Password!',
        )
