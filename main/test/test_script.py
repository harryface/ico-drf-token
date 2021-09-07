from faker import Faker
from django.test import TestCase
from django.utils import timezone

from main.models import CustomUser, Bid, SiteConfiguration, SuccessfulBid, UnSuccessfulBid
from script import distributor


class ScriptTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        faker = Faker()

        d = [[200, 1500, 7.5, 4], [200, 800, 4, 4], [
            300, 720, 2.4, 4], [200, 480, 2.4, 4], [300, 400, 2, 4], ]
        for i in range(5):
            user = CustomUser.objects.create(email=faker.email(), password="")
            Bid.objects.create(
                user=user,
                number_of_tokens=d[i][0],
                bidding_price=d[i][1],
                unit_price=d[i][2],
                created_at=(
                    timezone.now() - timezone.timedelta(hours=d[i][3])
                )
            )

        cls.site_conf = SiteConfiguration.objects.create(
            available_token=657,
            distributed=False,
            start_date=timezone.now() - timezone.timedelta(seconds=86400),
            end_date=timezone.now()
        )

        cls.script = distributor

    def test_script_works(self):
        " Test distributing token script works."
        self.script.start()

        self.assertEqual(200, SuccessfulBid.objects.get(id=1).token_allotted)
        self.assertEqual(200, SuccessfulBid.objects.get(id=2).token_allotted)
        self.assertEqual(129, SuccessfulBid.objects.get(id=3).token_allotted)
        self.assertEqual(128, SuccessfulBid.objects.get(id=4).token_allotted)
        self.assertEqual(4, SuccessfulBid.objects.all().count())
        self.assertEqual(1, UnSuccessfulBid.objects.all().count())
        self.assertEqual(0, SiteConfiguration.objects.get(
            id=self.site_conf.id).available_token)
