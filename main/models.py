from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save

from ico_crypcentra import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.is_examiner = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_examiner = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    '''Assign UserModelManager as the default object manager.'''
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @property
    def name(self):
        return self.email

    def __str__(self):
        return self.email


class Bid(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='bids')
    number_of_tokens = models.IntegerField(default=1)
    bidding_price = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0.00, editable=False)
    created_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.bid.id} made by {self.user}"


class SuccessfulBid(models.Model):
    bid = models.ForeignKey(
        Bid, on_delete=models.CASCADE)
    token_allotted = models.IntegerField(default=1)

    def __str__(self):
        return self.bid


class UnSuccessfulBid(models.Model):
    bid = models.ForeignKey(
        Bid, on_delete=models.CASCADE)

    def __str__(self):
        return self.bid


class SiteConfiguration(models.Model):
    coin_name = models.CharField(max_length=100, default="Crypcentra")
    available_token = models.IntegerField(default=5000)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    distributed = models.BooleanField(
        help_text="NB: This ought to be false at instantiation.", default=False)

    @property
    def is_within_window(self):
        return self.start_date <= timezone.now() <= self.end_date

    def save(self, *args, **kwargs):
        # check if another instance exists and throw an error.
        if not self.pk and SiteConfiguration.objects.exists():
            raise ValidationError(
                'There is can be only one SiteConfiguration instance')
        return super().save(*args, **kwargs)


def pre_save_complete(sender, instance, *args, **kwargs):
    if not instance.unit_price:
        # calculate the unit price
        instance.unit_price = instance.bidding_price/instance.number_of_tokens
    if not instance.created_at:
        # populate the timestamp
        instance.created_at = timezone.now()


pre_save.connect(pre_save_complete, sender=Bid)
