from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addListing", views.add, name="add"),
    path("<str:name>/", views.ListingsPage, name="cool"),
    path("watchlist", views.watchList, name="watchlist"),
    path("category/<str:ss>/", views.categories, name="category"),
    path("category", views.category, name="categories")
]
