from auctions.models import Auction, Bid, Comment, Watchlist
from django.contrib import admin

# Register your models here.

admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
