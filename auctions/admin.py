from django.contrib import admin
from .models import User, AuctionListing, Bid

# FIRST OPTION:::
# Register your models here.
# admin.site.register(User)
# admin.site.register(AuctionListing)
# admin.site.register(Bid)


# SECOND OPTION:::
# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'starting_bid', 'current_bid', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('title', 'description')

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'amount', 'time')
    list_filter = ('time',)
    search_fields = ('listing__title', 'bidder__username')

class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)  # Note the comma - makes it a tuple

admin.site.register(User, UserAdmin)  # Pass UserAdmin here
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
