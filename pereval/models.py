from django.db import models

from . import StatusNames


class CustomUser(models.Model):
    email = models.EmailField()
    fam = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    otc = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Pereval(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    beauty_title = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    other_titles = models.CharField(max_length=150)
    connect = models.TextField(blank=True)

    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)

    winter = models.CharField(max_length=50, blank=True)
    summer = models.CharField(max_length=50, blank=True)
    autumn = models.CharField(max_length=50, blank=True)
    spring = models.CharField(max_length=50, blank=True)

    status = models.CharField(max_length=150, default=StatusNames.NEW, choices=StatusNames.CHOICES)

    add_time = models.DateTimeField(auto_now_add=True)


class Images(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=150)
    path = models.ImageField(upload_to="uploads/perevals")
