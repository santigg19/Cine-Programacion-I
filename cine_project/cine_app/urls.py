from django.conf.urls import url
from django.urls import path
from cine_app import views
from .views import MovieAPIView, MovieDetails, index, HallAPIView, HallDetails, ProjectionAPIView, ActiveProjectionAPIView, MovieTimeAPIView, movie_fechas, ProjectionTimeAPIView

urlpatterns = [

    path('', index, name='index'),


    # Endpoint Peliucla
    path('movie/', MovieAPIView.as_view()),                     # OK Retorna    peliculas
    path('detail/<int:id_movie>/', MovieDetails.as_view()),     # OK            pelicula en particular por id
    path('movietime/', MovieTimeAPIView.as_view()),             # OK            peliculas en un rango de 8 dias

    # Ejemplo http://localhost:8000/moviedate/DjangoUnchained/2020-12-15/2020-12-25
    url(r'^moviedates/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.movie_fechas),

    # Endpoint Sala
    path('hall/', HallAPIView.as_view()),                       # OK            salas
    path('halldetail/<int:id_hall>/', HallDetails.as_view()),   # OK            sala por id

    # Trae las proyecciones
    path('projections/', ProjectionAPIView.as_view()),
    path('activeprojections/', ActiveProjectionAPIView.as_view()),   # OK
    path('projectionstime/', ProjectionTimeAPIView.as_view()), # Proyecciones en un rango de 2 semanas

]
