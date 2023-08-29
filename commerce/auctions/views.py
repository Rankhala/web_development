from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListings, Bid, Comment, Category


def index(request):
    allListings = AuctionListings.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
            "listings": allListings,
            "allCategories": allCategories
        })

@login_required
def new_listing(request):
    allCategories = Category.objects.all()
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        description = request.POST["description"]
        imageurl = request.POST.get("Imageurl")
        category = request.POST["category"]
        user = request.user

        categoryQuery = Category.objects.get(category_name=category)

        #Create a bid object
        bid = Bid(bid_price=price, user=user)
        bid.save()

        new = AuctionListings(
                listing_name = name,
                lister_name = user,
                price = float(bid),
                description = description,
                imageURL = imageurl,
                category = categoryQuery
            )

        new.save()

        return HttpResponseRedirect(reverse("auctions:index"))

    else:
        return render(request, "auctions/listing.html", {
                "allCategories": allCategories
            })

def display_category(request):
    if request.method == "POST":
        selected_category = request.POST["category"]
        category = Category.objects.get(category_name=selected_category)
        allListings = AuctionListings.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
                "listings": allListings,
                "allCategories": allCategories
            })

def item_info(request, id):
    item_data = AuctionListings.objects.get(pk=id)
    isItemInWatchList = request.user in item_data.watch_list.all()
    all_comments = Comment.objects.filter(listing=item_data)
    bid_data = Bid.objects.filter(item=item_data)
    return render(request, "auctions/item.html", {
            "item": item_data,
            "isItemInWatchList": isItemInWatchList,
            "all_comments": all_comments
        })

def removeItem(request, id):
    listing_data = AuctionListings.objects.get(pk=id)
    current_user = request.user
    listing_data.watch_list.remove(current_user)
    return HttpResponseRedirect(reverse("auctions:item",args=(listing_data.id, ))) 

def addItem(request, id):
    listing_data = AuctionListings.objects.get(pk=id)
    current_user = request.user
    listing_data.watch_list.add(current_user)
    return HttpResponseRedirect(reverse("auctions:item",args=(listing_data.id, )))

def display_watchlist(request):
    current_user = request.user
    user_listing = current_user.user.all()
    return render(request, "auctions/watchlist.html", {
            "listings": user_listing
        })

def add_comment(request, id):
    current_user = request.user
    listing_data = AuctionListings.objects.get(pk=id)
    comment = request.POST["comment"]

    new_comment = Comment(
            comment_text = comment,
            author = current_user,
            listing = listing_data
        )
    new_comment.save()

    return HttpResponseRedirect(reverse("auctions:item", args=(listing_data.id, )))

def add_bid(request, id):
    listing_data = AuctionListings.objects.get(pk=id)
    current_user = request.user
    bidding_price = request.POST["bid"]

    if int(bidding_price) > listing_data.price:
        new_bid = Bid(bid_price=price, user=current_user, item=listing_data)
        new_bid.save()
        listing_data.price = new_bid
        listing_data.save()

        return render(request, "auctions/item.html", {
                "message": "Bid placed successfully!"
            })
    else:
        return render(request, "auctions/item.html", {
                "message": "Bid must be higher than current bid!"
            })


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
