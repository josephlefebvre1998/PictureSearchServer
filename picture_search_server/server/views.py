from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from process import searchVGG
from keras.preprocessing import image
from django.contrib.sites.shortcuts import get_current_site


import os
import datetime

from server.models import Results
from server.models import ImgSearchObject
from server.serializers import ImgSearchSerializer


# Create your views here.
class ImgSearches(APIView):

    def post(self, request):
        errors = {"error": "Image must not be empty"}
        data = request.data
        # if len(data) is not 0:
        try:
            img = data["image"]
            try:
                max_res = int(data["max_res"])
            except KeyError:
                max_res = 3

            # Set request date
            date_hour = datetime.datetime.now()
            date = date_hour.strftime('%Y-%m-%d %H:%M:%S')

            # Set request client
            client = request.META['HTTP_USER_AGENT']

            # Create entity
            img_search_object = ImgSearchObject.objects.create(date=date, client=client, image=img)

            # Save entity
            img_search_object.save()

            img_to_process = image.load_img(img_search_object.image, target_size=(150, 150))

            # predict_results(img_to_process,img_search_object)
            results = searchVGG.predict(img_to_process, max_res=3)
            print(results)

            # Save results
            for result,score in results:

                elmts = result.decode().split("/")
                result = result.decode()
                result = result.replace("i", "I", 1)
                res = Results(label=elmts[2], score=score,
                              url=result)
                res.save()
                img_search_object.results.add(res)

            if True:
                response = Response(status=status.HTTP_201_CREATED)
                response['location'] = "http://"+get_current_site(request).domain+img_search_object.get_absolute_url()
                return response
        except KeyError:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        img_searches = ImgSearchObject.objects.all()
        serializer = ImgSearchSerializer(img_searches, many=True)
        return Response(serializer.data)

    def predict_results(img_to_process,img_search_object,max_res=3):
        # Predict results
        results = searchVGG.predict(img_to_process, max_res)
        print(results)

        # Save results
        for result,score in results:

            elmts = result.decode().split("/")
            result = result.decode()
            result = result.replace("i", "I", 1)
            res = Results(label=elmts[2], score=score,
                            url=result)
            res.save()
            img_search_object.results.add(res)

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
