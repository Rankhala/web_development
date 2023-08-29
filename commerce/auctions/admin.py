from django.contrib import admin
from .models import Category, AuctionListings, Bid, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(AuctionListings)
admin.site.register(Bid)
admin.site.register(Comment)