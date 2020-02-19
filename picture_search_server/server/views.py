from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from process import searchVGG
from keras.preprocessing import image
from django.contrib.sites.shortcuts import get_current_site


import os

from server.models import Results
from server.models import ImgSearchObject
from server.serializers import ImgSearchSerializer


# Create your views here.
class ImgSearches(APIView):

    def post(self, request):
        # searchVGG.predict_test()
        errors = {"error": "body must not be empty"}
        data = request.data
        # if len(data) is not 0:
        if True:
            # print(data["date"])
            img_path = os.path.normpath(os.path.join(os.getcwd(), "./tests_images/elephant.jpg"))

            image_load = image.load_img(img_path, target_size=(150, 150))
            results = searchVGG.predict(image_load)
            data["image"] = img_path
            data["date"] = "2020-01-01T10:10"
            data["client"] = "AndroidFront"
            # serializer = ImgSearchSerializer(data=data)
            img_search_object = ImgSearchObject()
            img_search_object.image = data["image"]
            img_search_object.date = data["date"]
            img_search_object.client = data["client"]
            img_search_object.save()
            print(results)
            for result in results:
                elmts = result.decode().split("/")
                res = Results(label=elmts[2], score=0,
                              url=result)
                res.save()
                img_search_object.results.add(res)

            # img_search_object.results.set(results)
            # serializer = ImgSearchSerializer(data=data)
            # if serializer.is_valid():
            if True:
                response = Response(status=status.HTTP_201_CREATED)
                response['location'] = "http://"+get_current_site(request).domain+img_search_object.get_absolute_url()
                return response
            # errors = serializer.errors
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
