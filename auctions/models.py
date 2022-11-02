from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Hack(models.Model):
    listing_count = models.IntegerField(default=0)
    watchlist_count = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='hack')

    def active_count(self):
        return sum([h.listing_count for h in Hack.objects.all()])
