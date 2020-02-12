from django.db import models
from rest_framework import serializers
from server.models import ImgSearchObject
from server.models import Results


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Results
        fields = ('id', 'label', 'score', 'url')


class ImgSearchSerializer(serializers.ModelSerializer):

    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = ImgSearchObject
        fields = ('id', 'image', 'date', 'client', 'results')
