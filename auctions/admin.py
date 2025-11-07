from django.contrib import admin
from .models import User, AuctionListing, Bid


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'starting_bid', 'current_bid', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('title', 'description')

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'amount', 'time')
    list_filter = ('time',)
    search_fields = ('listing__title', 'bidder__username')

class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',) 

admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
