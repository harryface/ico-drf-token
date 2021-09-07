from django.utils import timezone
from main.models import SiteConfiguration
from random import choice
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .factory import UserFactory


class BidTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.user=UserFactory.create()
        cls.sc = SiteConfiguration.objects.create(start_date=timezone.now(), end_date=timezone.now()+timezone.timedelta(seconds=5000))
        cls.bid_url = reverse('bid')

    def test_if_data_is_correct_then_create(self):
        # Prepare data
        bid_dict = {
            'number_of_tokens': choice([10, 20, 30, 40, 50]),
            'bidding_price': choice([1000, 2000, 3000, 4000, 5000]),
        }
        # authenticate
        self.client.force_authenticate(user=self.user)
        # Make request
        response = self.client.post(self.bid_url, bid_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_bidding_price_is_smaller_it_fails(self):
        # Prepare data with already saved user
        bid_dict = {
            'bidding_price': choice([10, 20, 30, 40, 50]),
            'number_of_tokens': choice([1000, 2000, 3000, 4000, 5000]),
        }
        # authenticate
        self.client.force_authenticate(user=self.user)
        # Make request
        response = self.client.post(self.bid_url, bid_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ExternalBidTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.user=UserFactory(is_superuser=True, is_staff=True)
        cls.sc = SiteConfiguration.objects.create(start_date=timezone.now(), end_date=timezone.now()+timezone.timedelta(seconds=5000))
        cls.bid_url = reverse('external_bid')

    def test_if_user_is_not_admin_then_fail(self):
        ordinary_user = UserFactory.create()
        # Prepare data
        bid_dict = [{
            'user': self.user.id,
            'number_of_tokens': choice([10, 20, 30, 40, 50]),
            'bidding_price': choice([1000, 2000, 3000, 4000, 5000]),
            'created_at': timezone.now()
        }]
        # authenticate
        self.client.force_authenticate(user=ordinary_user)
        # Make request
        response = self.client.post(self.bid_url, bid_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            str(response.data['detail']),
            'You do not have permission to perform this action.',
        )        

    def test_if_data_is_correct_then_create(self):
        # Prepare data
        bid_dict = [{
            'user': self.user.id,
            'number_of_tokens': choice([10, 20, 30, 40, 50]),
            'bidding_price': choice([1000, 2000, 3000, 4000, 5000]),
            'created_at': timezone.now(),
        }]
        # authenticate
        self.client.force_authenticate(user=self.user)
        # Make request
        response = self.client.post(self.bid_url, bid_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_bidding_price_is_smaller_it_fails(self):
        # Prepare data with already saved user
        bid_dict = [{
            'user': self.user.id,
            'bidding_price': choice([10, 20, 30, 40, 50]),
            'number_of_tokens': choice([1000, 2000, 3000, 4000, 5000]),
            'created_at': timezone.now(),
        }]
        # authenticate
        self.client.force_authenticate(user=self.user)
        # Make request
        response = self.client.post(self.bid_url, bid_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
