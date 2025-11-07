from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import BidForm

from .models import User, AuctionListing, Bid, Comments


def index(request):
    # Retrieve all auction listings, ordered by creation date/time
    listings = AuctionListing.objects.filter(active=True).order_by('-created_at')
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    # Check if the user is logged in
    if not request.user.is_authenticated:
        return render(request, "auctions/create_listing.html", {"message": "User Must Be Logged in First"})

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        starting_bid = request.POST.get("starting_bid", "").strip()
        image_url = request.POST.get("image_url", "").strip()

        # Create a new Auction Listing
        listing = AuctionListing.objects.create(
            title=title, 
            description=description, 
            starting_bid=starting_bid, 
            image_url=image_url,
            owner=request.user
        )

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html")
    

def listing(request, listing_id):
    try:
        listing = AuctionListing.objects.get(id=listing_id)
    except AuctionListing.DoesNotExist:
        return render(request, "auctions/index.html", {
            "message": "Listing not found."
        })
    
    if request.method == 'POST':
        form = BidForm(request.POST, listing=listing)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.listing = listing
            bid.bidder = request.user
            bid.save()
            return redirect("listing", listing_id=listing.id)
    else:
        form = BidForm(listing=listing)
        
    return render(request, "auctions/listing.html", {
        "listing": listing, "bid_form": form
    })

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    
    if request.user != listing.owner:
        return HttpResponse("Unauthorized", status=403)

    listing.closed = True
    listing.create_winner()
    listing.save()
    return redirect("listing", listing_id=listing.id)

@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    user = request.user

    if listing in user.watchlist.all():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)

    return redirect('listing', listing_id=listing.id)


@login_required
def watchlist(request):
    watchlist_items = request.user.watchlist.all()
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items
    })
