from rest_framework import serializers
from .models import Movie, Hall, Projection, Seats

#PELICULA
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        #fields = ['id', 'name', 'duration', 'description', 'detail', 'genre', 'classification', 'state', 'start_date', 'finish_date']
        fields = '__all__'

#SALA
class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

#PROYECCION
class ProjectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projection
        fields = '__all__'

#ASIENTO
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = '__all__'
