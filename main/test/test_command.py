from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model

from main.models import Bid, SiteConfiguration


class CommandsTestCase(TestCase):
    def test_populate_site_command(self):
        " Test populate site command."

        call_command('populate_site')

        self.assertEqual(True, SiteConfiguration.objects.all().exists())
        self.assertEqual(300, get_user_model().objects.all().count())
        self.assertEqual(300, Bid.objects.all().count())
