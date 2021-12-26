from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new"),
    path("new/save", views.save_listing, name="save-listing"),
    path("view_listing/delete", views.delete_listing, name="delete-listing"),
    path("view_listing", views.view_listing, name="view-listing"),
    path("view_listing/add_to_watchlist", views.watchlist, name="watch-list"),
    path("view_listing/comment", views.comment, name="comment"),
    path("view_listing/bid", views.bid, name="bid"),
    path("view_watchlist", views.view_watchlist, name="view-watchlist"),
    path("view_watchlist/delete_item", views.delete_watch_item, name="delete-watch-item"),
    path("categories", views.categories, name="categories"),
    path("categories/view-category", views.view_category, name="view-category")
]
