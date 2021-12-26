from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import related
from django.db.models.fields.files import ImageField


class User(AbstractUser):
    pass


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE,
                             related_name="user", null=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=200, null=True)
    category = models.CharField(max_length=100)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.title} (auction price: ${self.price})"


class Bid(models.Model):
    item = models.ForeignKey(Auction, on_delete=CASCADE,
                             related_name='bid_item', null=True)
    bidder = models.ForeignKey(
        User, on_delete=CASCADE, related_name='bidder', null=True)
    bid_price = models.FloatField(null=True)

    def __str__(self):
        return f"${self.bid_price} Bid placed on {self.item} by {self.bidder}"


class Comment(models.Model):
    comment_item = models.ForeignKey(
        Auction, on_delete=CASCADE, related_name="item", null=True)
    commentator = models.ForeignKey(
        User, on_delete=CASCADE, related_name="comment_by", null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return f"Comment: {self.comment} on {self.comment_item}, by {self.commentator}"
    # pass
    # comment_title = models.CharField(max_length=100)
    # comment_content = models.CharField(max_length=1000)


class Watchlist(models.Model):
    watcher = models.ForeignKey(
        User, on_delete=CASCADE, related_name="watcher", null=True)
    watch_item = models.ForeignKey(
        Auction, on_delete=CASCADE, related_name="watch_item", null=True)

    def __str__(self):
        return f"{self.watch_item}"
