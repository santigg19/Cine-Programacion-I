# Generated by Django 3.1.1 on 2020-12-12 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id_hall', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('state', models.CharField(choices=[('HABILITADA', 'Habilitada'), ('DESHABILITADA', 'Deshabilitada'), ('ELIMINADA', 'Eliminada')], default='HABILITADA', max_length=15)),
                ('row', models.PositiveSmallIntegerField()),
                ('seat', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id_movie', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('duration', models.IntegerField()),
                ('description', models.CharField(max_length=500)),
                ('detail', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=50)),
                ('classification', models.CharField(choices=[('G', 'Publico General'), ('PG', 'Guia Parental Sugerida'), ('PG-13', 'Mayores de 13'), ('R', 'Menores de 16 requieren asistir con un adulto'), ('NC-17', 'Mayores de 18')], default='PG', max_length=50)),
                ('state', models.CharField(choices=[('ACTIVO', 'Activo'), ('NO ACTIVO', 'No Activo')], default='NO ACTIVO', max_length=12)),
                ('start_date', models.DateField(verbose_name='Inicio')),
                ('finish_date', models.DateField(verbose_name='Fin')),
            ],
        ),
        migrations.CreateModel(
            name='Projection',
            fields=[
                ('id_projection', models.AutoField(primary_key=True, serialize=False)),
                ('date_zero', models.DateField(verbose_name='Inicio')),
                ('date_final', models.DateField(verbose_name='Fin')),
                ('time_projection', models.TimeField()),
                ('state', models.CharField(choices=[('ACTIVO', 'Activo'), ('NO ACTIVO', 'No Activo')], default='ACTIVO', max_length=12)),
                ('hall', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cine_app.hall')),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cine_app.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Seats',
            fields=[
                ('id_seats', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('row', models.SmallIntegerField()),
                ('seat', models.SmallIntegerField()),
                ('projection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cine_app.projection')),
            ],
        ),
    ]