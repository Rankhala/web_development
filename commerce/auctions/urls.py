from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.new_listing, name="listing"),
    path("display_category", views.display_category, name="display_category"),
    path("item/<int:id>", views.item_info, name="item"),
    path("remove/<int:id>", views.removeItem, name="remove"),
    path("add/<int:id>", views.addItem, name="add"),
    path("watchlist", views.display_watchlist, name="watchlist"),
    path("comment/<int:id>", views.add_comment, name="comment"),
    path("bid/<int:id>", views.add_bid, name="bid")
]
