from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass


class Category(models.Model):
    idC = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name

class Listing(models.Model):
    idL = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_bid = models.FloatField()
    is_active = models.BooleanField(default=True)
    link = models.TextField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userid")
    date = models.DateTimeField(default=datetime.datetime.now)
    categories = models.ManyToManyField(Category, blank=False, related_name="categories")
    
    def __str__(self):
        return self.title
    

class Bid(models.Model):
    idB = models.AutoField(primary_key=True)
    bid = models.FloatField()
    date = models.DateTimeField(default=datetime.datetime.now)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userbidid")
    id_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingid")

    def __str__(self):
        return f"self.idB"

class Comment(models.Model):
    idCo = models.AutoField(primary_key=True)
    name = models.TextField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userCommentid")
    id_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingCommentid")

    def __str__(self):
        return self.name
    

class WatchList(models.Model):
    idW = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userwlistid")
    listings = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"self.idW"




    
    
