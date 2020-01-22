from django.db import models
from rest_framework import serializers
from server.models import ImgSearchObject


class ImgSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImgSearchObject
        fields = ('id', 'image', 'date', 'client')