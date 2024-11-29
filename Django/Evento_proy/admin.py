from django.contrib import admin
from .models import Concierto, Conferencia  # Importar los modelos correctos

admin.site.register(Concierto)
admin.site.register(Conferencia)