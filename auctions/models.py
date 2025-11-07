from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        "AuctionListing", blank=True, related_name="watchlisted_by"
    )

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid  = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="won_auctions")
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def current_bid(self):
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            return highest_bid.amount
        return self.starting_bid
    
    def bid_count(self):
        return self.bids.count()
    
    def create_winner(self):
        if self.closed:
            highest_bid = self.bids.order_by('-amount').first()
            if highest_bid:
                self.winner = highest_bid.bidder
                self.save()
            return self.winner

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} bid ${self.amount} on {self.listing.title}"

class Comments():
    pass

