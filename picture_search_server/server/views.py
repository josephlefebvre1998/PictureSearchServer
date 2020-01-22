from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from server.models import ImgSearchObject
from server.serializers import ImgSearchSerializer


# Create your views here.
class ImgSearches(APIView):

    def post(self, request):
        errors = {"error": "body must not be empty"}
        if len(request.data) is not 0:
            serializer = ImgSearchSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                response = Response(serializer.data, status=status.HTTP_201_created)
                response['location'] = obj.get_absolute_url()
                return response
            errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        img_searches = ImgSearchObject.objects.all()
        serializer = ImgSearchSerializer(img_searches, many=True)
        return Response(serializer.data)


class ImgSearch(APIView):

    def get_object(self, pk):
        try:
            return ImgSearchObject.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        img_searches = self.get_object(pk)
        serializer = ImgSearchSerializer(img_searches)
        return Response(serializer.data)

    def post(self, request, format=None):
        if len(request.data) is not 0:
            serializer = ImgSearchSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                response = Response(serializer.data, status=status.HTTP_201_created)
                response['location'] = obj.get_absolute_url()
                return response
            errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
