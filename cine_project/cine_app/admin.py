#from django.contrib import admin

# Register your models here.



from django.contrib import admin
from .models import Movie, Hall, Projection, Seats


admin.site.register(Movie)
admin.site.register(Hall)
admin.site.register(Seats)
admin.site.register(Projection)
