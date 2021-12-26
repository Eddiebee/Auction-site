from re import T
import re
from django import http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models.fields import related
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import Http404
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
from .models import Auction, Bid, Comment, User, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "auction_listings": Auction.objects.all()
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


@login_required
def new_listing(request):

    # return HttpResponse("good to go!")
    return render(request, "auctions/new-listing.html", {
       "auction_listings": Auction.objects.all()
    })

def save_listing(request):
    if request.method == "POST":
        # data = request.POST.get("title")
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["starting-bid"]
        # image = request.FILES["image"]
        user_id = int(request.POST["user"])
        url = request.POST["url"]
        category = request.POST["category"]
        time = request.POST["time"]
        
        user = User.objects.get(pk=user_id)
        
        # fs = FileSystemStorage()
        # filename = fs.save(image.name, image)
        # image = fs.url(filename)
        Auction.objects.create(title=title, description=description, 
                                price=price, url=url, user=user, category=category, time=time)

        # aucton = Auction.objects.get(category)
        # a = Auction(title=data.title)

    return HttpResponseRedirect(reverse("index"))
    # return HttpResponse(f"<center><h1>{title} <br> Good to GO!</h1> </center>")

def delete_listing(request):
    if request.method == "POST":
        auction_id = request.POST['id']

        item = Auction.objects.get(pk=auction_id)

        bidders = []
        bids = Bid.objects.filter(item=auction_id)
        for bid in bids:
            bidders.append(bid.bidder)


    return HttpResponse(f"{item}<h1> Why you wan delete me?  {bids}</h1>")

def view_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        auction_id = request.POST["id"]

        # getting the highest bidder
        highest_bid = Bid.objects.filter(item=auction_id).aggregate(Max('bid_price'))

        highest_bid_amt = highest_bid['bid_price__max']
        try:
            winner = Bid.objects.get(bid_price=highest_bid_amt)
        except:
            winner = 'none yet'
            pass
            # raise Http404("No bid price avaialable!")


    return render(request, "auctions/view-listing.html", {
        "auction_listing": Auction.objects.get(pk=auction_id),
        "watchlists": Watchlist.objects.filter(watch_item=auction_id),
        "bids": Bid.objects.filter(item=auction_id),
        "winner": winner,
        # "ok": ok,
        # "winner": Bid.objects.get(bid_price=highest_bidder),
        # "winner": Bid.objects.filter(b),
        "comments": Comment.objects.filter(comment_item=auction_id),
        "title": title,
        "auction_id": auction_id,
        # "lister": auction_creator
    })

def watchlist(request):
    if request.method == "POST":
        item_id = request.POST["id"]
        watcher_id = request.POST["watcher"]
        item = Auction.objects.get(pk=item_id)
        watcher = User.objects.get(pk=watcher_id)

        if not Watchlist.objects.filter(watch_item=item, watcher=watcher):
            Watchlist.objects.create(watch_item=item, watcher=watcher)
        else:
            return HttpResponse("item already in watch list")


        return HttpResponseRedirect(reverse("view-watchlist"))


def view_watchlist(request):

    return render(request, "auctions/watchlist.html", {
        # "watchlists": Watchlist.objects.all(),
        "watchlist": Watchlist.objects.filter(watcher=request.user)
    })


def delete_watch_item(request):
    
    if request.method == 'POST':
        item_id = request.POST["id"]
        title = request.POST["title"]

    watchlist = Watchlist.objects.get(watch_item_id=item_id, watcher=request.user)
    toCheck = Auction.objects.get(pk=item_id)

    Watchlist.objects.get(watch_item_id=item_id, watcher=request.user).delete()
    # return HttpResponse("DONE!")
    return HttpResponseRedirect(reverse("view-watchlist"))


def comment(request):

    if request.method == "POST":
        item_id = int(request.POST['item_id'])
        user_id = request.POST['user_id']
        text = request.POST['comment']

        item = Auction.objects.get(id=item_id)
        user = User.objects.get(id=user_id)
        
        # create comment
        Comment.objects.create(comment_item=item, commentator=user, comment=text)

    return HttpResponse(f"<center><h1>You too dey talk!!</h1> <br>SUCCESS<br> {user} commented on  {item}! <br> Comment: {text}</center>")


def bid(request):
    if request.method == 'POST':
        item_id = request.POST['id']
        bid_price = float(request.POST['bid-price'])
        bidder_id = request.POST['bidder']
        starting_bid = float(request.POST['price'])

        item = Auction.objects.get(pk=item_id)
        bidder = User.objects.get(pk=bidder_id)

        
        biddings = []
        bids = Bid.objects.filter(item=4)

        for bid in bids:
            biddings.append(bid.bid_price)

        for i in biddings:
            float(i)
            if (bid_price > i) and (bid_price >= starting_bid):
                Bid.objects.create(item=item, bidder=bidder, bid_price=bid_price)
                return render(request, "auctions/bid.html", {
                    "success": f"Hey, {request.user}, your bid was succesful!",
                })
            else:
                raise Http404('Your bidding must be as large as the starting bid and greater than all other biddings.')


def categories(request):
    auction_listings = Auction.objects.all()
    return render(request, "auctions/categories.html", {
        "auction_listings": auction_listings
    })
    # return HttpResponse("<h1>Categories</h1>")

def view_category(request):

    if request.method == 'POST':
        category = request.POST['category-name']

    cates = Auction.objects.filter(category=category)

    return render(request, 'auctions/category-view.html', {
        "cates": cates
    })
    # return HttpResponse(f"<h1>{cate.id} View Category</h1>")

        