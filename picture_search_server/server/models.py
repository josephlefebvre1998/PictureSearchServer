from django.db import models
from django.urls import reverse


# Create your models here.
class Results(models.Model):
    label = models.CharField(max_length=100, blank=True, default='')
    score = models.FloatField()
    url = models.CharField(max_length=100, blank=True, default='')


class ImgSearchObject(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    date = models.DateTimeField(auto_now_add=False)
    client = models.CharField(max_length=100, blank=True, default='')
    results = models.ManyToManyField(Results)

    # def get_absolute_url(self):
    #     return "/imh_searches/%i/" % self.pk
    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('date',)