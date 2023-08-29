from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name

class Bid(models.Model):
    bid_price = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddingUser")

class AuctionListings(models.Model):
    listing_name = models.CharField(max_length=64)
    lister_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listerUsername")
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="biddingPrice")
    description = models.CharField(max_length=350)
    isActive = models.BooleanField(default=True)
    imageURL = models.URLField(max_length=350)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="itemCategory")
    watch_list = models.ManyToManyField(User, blank=True, null=True, related_name="user")

    def __str__(self):
        return f"{self.listing_name} listed by {self.lister_name}"

class Comment(models.Model):
    comment_text = models.CharField(max_length=350)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentAuthor")
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="listingComment")

    def __str__(self):
        return f"Written by {self.author}"