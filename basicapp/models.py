from django.db import models


# Create your models here.

class userinfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=100)
    room_no = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_no = models.BigIntegerField()


class Bookings(models.Model):
    user = models.CharField(max_length=40)
    date = models.CharField(max_length=10)
    startpt = models.CharField(max_length=40)
    lastpt = models.CharField(max_length=40)
    cht = models.CharField(max_length=40)
    tot = models.CharField(max_length=40)


class contact_us(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=75)
    subject = models.TextField()
    feed = models.TextField()


class discount(models.Model):
    img = models.ImageField(upload_to='discount_img')
    offer_on = models.CharField(max_length=40)
    code = models.CharField(max_length=40)
    offer = models.BooleanField(default=False)
    dis_amt = models.IntegerField(default=10)


class cycles(models.Model):
    img = models.ImageField(upload_to='cycle_img')
    name = models.CharField(max_length=40)
    details = models.CharField(max_length=300)
    available = models.BooleanField(default=False)


class accessories(models.Model):
    img = models.ImageField(upload_to='accesories')
    name = models.CharField(max_length=40)
    price = models.IntegerField(default=10)
