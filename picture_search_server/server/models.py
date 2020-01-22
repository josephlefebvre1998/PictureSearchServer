from django.db import models


# Create your models here.
class Results(models.Model):
    label = models.CharField(max_length=100, blank=True, default='')
    score = models.DecimalField(max_digits=10,decimal_places=8)
    url = models.CharField(max_length=100, blank=True, default='')


class ImgSearchObject(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    date = models.DateTimeField(auto_now_add=False)
    client = models.CharField(max_length=100, blank=True, default='')
    results = models.ManyToManyField(Results)

    class Meta:
        ordering = ('date',)