from django.db import models

# Create your models here.



class Movie(models.Model):
    id_movie = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    duration = models.IntegerField()
    description = models.CharField(max_length = 500)
    detail = models.CharField(max_length = 200)
    genre = models.CharField(max_length = 50)

    classifications = [
        ('G', 'Publico General'),
        ('PG', 'Guia Parental Sugerida'),
        ('PG-13', 'Mayores de 13'),
        ('R', 'Menores de 16 requieren asistir con un adulto'),
        ('NC-17', 'Mayores de 18'),
    ]
    classification = models.CharField(max_length = 50, choices=classifications, default='PG')

    active_or_not_active = [
        ('ACTIVO', 'Activo'),
        ('NO ACTIVO', 'No Activo'),
    ]
    state = models.CharField(max_length=12, choices=active_or_not_active, default='NO ACTIVO')

    start_date = models.DateField(verbose_name='Inicio')
    finish_date = models.DateField(verbose_name='Fin')

    def __str__(self):
        return self.name


class Hall(models.Model):
    id_hall = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)

    hall_states = [
        ('HABILITADA', 'Habilitada'),
        ('DESHABILITADA', 'Deshabilitada'),
        ('ELIMINADA', 'Eliminada'),
    ]
    state = models.CharField(max_length=15, choices=hall_states, default='HABILITADA')

    row = models.PositiveSmallIntegerField()
    seat = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Projection(models.Model):
    id_projection = models.AutoField(primary_key=True)

    hall = models.ForeignKey(Hall, null=True, blank=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    date_zero = models.DateField(verbose_name='Inicio')
    date_final = models.DateField(verbose_name='Fin')
    time_projection = models.TimeField()

    projection_states = [
        ('ACTIVO', 'Activo'),
        ('NO ACTIVO', 'No Activo'),
    ]
    state = models.CharField(max_length=12, choices=projection_states, default='ACTIVO')

    def __str__(self):
        show = "Pelicula: " + str(self.movie.name) + " | Sala: " + str(self.hall.name)
        return show


class Seats(models.Model):
    id_seats = models.AutoField(primary_key=True)
    projection = models.ForeignKey(Projection, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField()
    row = models.SmallIntegerField()
    seat = models.SmallIntegerField()

    def __str__(self):
        show = "Pelicula: " + str(self.projection.movie.name) + " | Fecha: " + str(self.date) + " | Fila Nro: " + str(self.row) + " | Asiento Nro: " + str(self.seat)
        return show


