from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
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


@login_required
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
 

@login_required
def add(request):
    if request.method == "POST":
        current_user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        img = request.POST["img"]
        category = request.POST["category"]
        
        user = User.objects.get(id=current_user.id)
        user.save()
        listing = Listing(title=title, description=description, starting_bid=float(bid), link=img, id_user=user)
        listing.save()
        c = Category.objects.get(name=category)
        listing.categories.add(c)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/addListing.html", {
        "categories": Category.objects.all()
        })
        
     
def ListingsPage(request, name):
    current_user = request.user
    listing = Listing.objects.get(title=name)
    if listing.is_active:
        coose = False
    else:
        coose = True
        high = Bid.objects.filter(id_listing=listing.idL).latest('bid')
        name = high.id_user.username
    if current_user.is_authenticated:
        user = User.objects.get(userid__pk=listing.idL)
        category = Category.objects.get(categories__pk=listing.idL)
        loggedUser = User.objects.get(id=current_user.id)
        if name:
            if loggedUser.username == name:
                return render(request, "auctions/listings.html", {
                    "listing": listing,
                    "username": user,
                    "category": category.name,
                    "bid": Bid.objects.filter(id_listing=listing.idL).count(),
                    "close": coose,
                    "msg": "Congratulation You win the bid."
                })
        if request.method == "POST":
            watchlist = request.POST.get('add', False)
            newBid = request.POST.get('newBid', False)
            close = request.POST.get('delete', False)
            comment = request.POST.get('comment', False)
            if newBid:
                newBid = float(newBid)
                if newBid > listing.starting_bid:
                    listing.starting_bid = newBid
                    listing.save()
                    bid = Bid(id_user=loggedUser, bid=newBid, id_listing=listing)
                    bid.save()
                    return render(request, "auctions/listings.html", {
                        "listing": listing,
                        "username": user,
                        "category": category.name,
                        "bid": Bid.objects.filter(id_listing=listing.idL).count(),
                        "close": coose
                    })
                else:
                    return render(request, "auctions/listings.html", {
                        "listing": listing,
                        "username": user,
                        "category": category.name,
                        "bid": Bid.objects.filter(id_listing=listing.idL).count(),
                        "message": "Error: The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed",
                        "close": coose
                    })
            if close:
                listing.is_active = False
                listing.save()
                coose = True
                return render(request, "auctions/listings.html", {
                    "listing": listing,
                    "username": user,
                    "category": category.name,
                    "bid": Bid.objects.filter(id_listing=listing.idL).count(),
                    "close" : coose
                })
            if watchlist:
                if WatchList.objects.get(id_user=loggedUser.id, listings=listing.idL):
                    WatchList.objects.filter(id_user=loggedUser.id, listings=listing.idL).delete()
                    return render(request, "auctions/listings.html", {
                        "listing": listing,
                        "username": user,
                        "category": category.name,
                        "bid": Bid.objects.filter(id_listing=listing.idL).count(),
                    "close" : coose
                    })
                else:    
                    listW = WatchList(id_user=loggedUser, listings=listing)
                    listW.save()
                    return render(request, "auctions/listings.html", {
                        "listing": listing,
                        "username": user,
                        "category": category.name,
                        "bid": Bid.objects.filter(id_listing=listing.idL).count(),
                        "close": coose
                    })
            if comment:
                cmt = Comment(name=comment, id_user=loggedUser, id_listing=listing)
                cmt.save()
                return render(request, "auctions/listings.html", {
                    "listing": listing,
                    "username": user,
                    "category": category.name,
                    "bid": Bid.objects.filter(id_listing=listing.idL).count(),
                    "close": coose,
                    "comments": Comment.objects.all()
                })
                    
            return render(request, "auctions/listings.html", {
                       "listing": listing,
                        "username": user,
                        "category": category.name,
                        "bid": Bid.objects.filter(id_listing=listing.idL).count(),
                "close": coose
                    })
        
        else:
            return render(request, "auctions/listings.html", {
                "listing": listing,
                "username": user,
                "category": category.name,
                "bid": Bid.objects.filter(id_listing=listing.idL).count(),
                "close": coose
            })
    else:
        return render(request, "auctions/listings.html", {
            "listing": listing,
            "username": user
        })
    
def watchList(request):
    current_user = request.user
    loggedUser = User.objects.get(id=current_user.id)
    List = WatchList.objects.filter(id_user=loggedUser.id)
    return render(request, "auctions/watchlist.html",{
        "list": List,
        "count": List.count()
    })

def categories(request, ss):
    cat = Category.objects.get(name=ss)
    listings = Listing.objects.filter(categories__pk=cat.idC)
    return render(request, "auctions/categories.html", {
        "categories": listings
    })
    
    
def category(request):
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all()
    })