from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from faker import Faker
from random import randrange
from main.models import Bid, SiteConfiguration


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        User = get_user_model()

        if not SiteConfiguration.objects.all().exists():
            SiteConfiguration.objects.create(
                start_date=timezone.now(),
                end_date=(
                    timezone.now() + timezone.timedelta(seconds=86400)
                    )
                )

        for _ in range(300):

            # create a user
            user = User.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                password='',
            )
            user.set_password('12345')
            user.save()

            # create one bid for the user
            Bid.objects.create(
                user=user,
                number_of_tokens=randrange(50, 100, 10),
                bidding_price=randrange(200, 500, 100),
                created_at=(
                    timezone.now() + timezone.timedelta(hours=randrange(5, 24))
                    )
            )
