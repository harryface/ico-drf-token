# factory.py inside users/test
from faker import Faker as FakerClass
from typing import Any, Sequence
from factory import django, Faker, post_generation

from ico_crypcentra import settings


class UserFactory(django.DjangoModelFactory):

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = (
            'email',
            'is_superuser',
            'is_staff'
        )

    is_superuser = False
    is_staff = False
    email = Faker('email')

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else FakerClass().password(
                length=30,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        self.set_password(password)
