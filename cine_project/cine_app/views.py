from django.shortcuts import render

from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Movie, Hall, Projection, Seats
from .serializers import MovieSerializer, HallSerializer, ProjectionSerializer, SeatSerializer
from rest_framework.decorators import api_view
import datetime as dt
from rest_framework.views import APIView
from rest_framework.response import Response
import re



# Create your views here.


def index(request):
    return HttpResponse("https://www.youtube.com/watch?v=nPuOmHpGH2o")


# Endpoint Peliculas
# OK

class MovieAPIView(APIView):
    
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class MovieTimeAPIView(APIView):
    
    def get(self, request):
        now = dt.datetime.now()
        time_range = dt.timedelta(days=8)
        peliculas = Movie.objects.filter(finish_date__gte=(now - time_range), start_date__lte=(now + time_range))
        #active_projections = Movie.objects.filter(state__gte=active)
        serializer = MovieSerializer(peliculas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# OK

class MovieDetails(APIView):

    def get_object(self, id_movie):
        try:
            return Movie.objects.get(id_movie=id_movie)

        except Movie.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id_movie):
        movie = self.get_object(id_movie)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, id_movie):
        movie = self.get_object(id_movie)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_movie):
        movie = self.get_object(id_movie)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# OK

class HallAPIView(APIView):
    
    def get(self, request):
        halls = Hall.objects.all()
        serializer = HallSerializer(halls, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HallSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# OK

class HallDetails(APIView):

    def get_object(self, id_hall):
        try:
            return Hall.objects.get(id_hall=id_hall)

        except Hall.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id_hall):
        hall = self.get_object(id_hall)
        serializer = HallSerializer(hall)
        return Response(serializer.data)

    def put(self, request, id_hall):
        hall = self.get_object(id_hall)
        serializer = HallSerializer(hall, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_hall):
        hall = self.get_object(id_hall)
        hall.delete()
        return Response({'SALA ELIMINADA'},status=status.HTTP_204_NO_CONTENT)


# OK
class ProjectionAPIView(APIView):
    
    def get(self, request):
        projections = Projection.objects.all()
        serializer = ProjectionSerializer(projections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Proyecciones activas
class ActiveProjectionAPIView(APIView):
    
    def get(self, request):
        active = 'ACTIVO'
        active_projections = Projection.objects.filter(state__gte=active)
        serializer = ProjectionSerializer(active_projections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Proyecciones activas de otra forma
@api_view(['GET'])
def projection_active(request):
    active = 'ACTIVO'
    active_projections = Projection.objects.filter(state__gte=active)
    projections_serializer = ProjectionSerializer(active_projections, many=True)
    return JsonResponse(projections_serializer.data, safe=False,
                        status=status.HTTP_200_OK)


# Proyecciones en un rango de 2 semanas
class ProjectionTimeAPIView(APIView):
    
    def get(self, request):
        now = dt.datetime.now()
        time_range = dt.timedelta(days=14)
        projections = Projection.objects.filter(date_final__gte=(now - time_range), date_zero__lte=(now + time_range))
        #active_projections = Movie.objects.filter(state__gte=active)
        serializer = ProjectionSerializer(projections, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def movie_fechas(request, name, start, finish):

    try:
        name = name_spaces(name)
        movies = Movie.objects.get(name=name, start_date=start, finish_date=finish)
        serializer = MovieSerializer(movies)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Movie.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


def name_spaces(moviename):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", moviename)

