from django.db import models

from . import StatusNames


class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    otc = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)

    def __str__(self):
        return self.email

    def get_fio(self):
        return f"{self.name} {self.otc} {self.fam}"

    def get_count_perevals(self):
        return self.pereval_set.count()


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    def get_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'height': self.height
        }


class Pereval(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    beauty_title = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    other_titles = models.CharField(max_length=150)
    connect = models.TextField(blank=True)

    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)

    winter = models.CharField(max_length=50, blank=True, null=True)
    summer = models.CharField(max_length=50, blank=True, null=True)
    autumn = models.CharField(max_length=50, blank=True, null=True)
    spring = models.CharField(max_length=50, blank=True, null=True)

    status = models.CharField(max_length=150, default=StatusNames.NEW, choices=StatusNames.CHOICES)

    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def get_level_dict(self):
        return {
            'winter': self.winter,
            'summer': self.summer,
            'autumn': self.autumn,
            'spring': self.spring
        }


class Images(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=150)
    path = models.ImageField(upload_to="uploads/perevals")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title
