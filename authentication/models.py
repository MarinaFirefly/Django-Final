from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class Customer(AbstractUser):
    # Customer is inherited from AbstactUser
    def __str__(self):
        return "{}".format(self.username)
    # additional field wallet
    wallet = models.DecimalField(max_digits=6, decimal_places=2, default=1000.00)

    def minus_wallet(self, payment):
        # when purchase is made
        self.wallet -= payment
        return self.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
