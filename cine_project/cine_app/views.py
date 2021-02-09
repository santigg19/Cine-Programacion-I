from abc import abstractmethod
from django.db.models.aggregates import Count
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


@api_view(['GET'])
def movie_time_range(request, name, start, finish):

    try:
        name = name_spaces(name)
        movies = Movie.objects.get(name=name, start_date=start, finish_date=finish)
        serializer = MovieSerializer(movies)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Movie.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


def name_spaces(moviename):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", moviename)


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



# Asientos


class SeatAPIView(APIView):
    
    def get(self, request):
        seats = Seats.objects.all()
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SeatSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeatsDetails(APIView):

    def get_object(self, id_seats):
        try:
            return Seats.objects.get(id_seats=id_seats)

        except Seats.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id_seats):
        seat = self.get_object(id_seats)
        serializer = SeatSerializer(seat)
        return Response(serializer.data)

    def put(self, request, id_seats):
        seat = self.get_object(id_seats)
        serializer = SeatSerializer(seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_seats):
        seat = self.get_object(id_seats)
        seat.delete()
        return Response({'SALA ELIMINADA'},status=status.HTTP_204_NO_CONTENT)




# Reporte de ventas en dos semanas
class ReportSalesTimeRange(APIView):
    
    def get(self, request):
        now = dt.datetime.now()
        time_range = dt.timedelta(days=14)
        tickets = Seats.objects.filter(date__gte=(now - time_range), date__lte=(now + time_range))
        serializer = SeatSerializer(tickets, many=True)
        sales = 0
        for ticket in tickets:
            sales += 1
        #return Response(serializer.data)   descomentar y cambiar por el otro return si se quiere retornar en detalle los asientos
        return Response({f'Se han vendido un total de {sales} tickets en un rango de 14 dias'})


# Reporte de ventas en tiempo y en una determinada proyeccion
class ReportProjectionTimeRange(APIView):
    def get_object(self, id_projection):
        try:
            return Projection.objects.get(id_projection=id_projection)

        except Projection.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id_projection):
        projection = Projection.objects.get(id_projection=id_projection)
        now = dt.datetime.now()
        time_range = dt.timedelta(days=14)
        tickets = Seats.objects.filter(date__gte=(now - time_range), date__lte=(now + time_range), projection=projection)
        how_many_tickets = tickets.count()

        return Response({f'En un rango de 14 dias se vendieron {how_many_tickets} tickets en la proyeccion de la pelicula {projection.movie.name}'})


# Reporte de ventas en peliculas activas

class ReportActiveMovies(APIView):

    def get(self, request):
        try:
            today = dt.date.today()
            movies = Movie.objects.filter(state='ACTIVO')
            show = []
            for movie in movies:
                how_many_tickets = 0
                projections = Projection.objects.filter(movie=movie)
                for projection in projections:
                    seats = Seats.objects.filter(projection=projection, date__lte=today)
                    how_many_tickets += seats.count()
                
                show.append({'Pelicula': movie.name, 'Tickets vendidos': how_many_tickets})

            return Response(show)

        except TypeError:
            return JsonResponse({'Message': 'The query is wrong'}, status=status.HTTP_404_NOT_FOUND)

