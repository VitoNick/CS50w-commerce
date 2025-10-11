from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid  = models.IntegerField()
    image_url = models.URLField()

class Bid():
    pass

class Comments():
    pass

