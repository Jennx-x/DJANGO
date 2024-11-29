from django.urls import path
from . import views

urlpatterns = [
    # Ruta para la página principal
    path('', views.index, name='index'),

    # Rutas para las acciones CRUD
    path('crear-evento/', views.crear_evento, name='crear_evento'),
    path('editar_evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('obtener_evento/', views.obtener_evento, name='obtener_evento'),
    path('eliminar-evento/', views.eliminar_evento, name='eliminar_evento'),
    path('calcular_costo_boletas/', views.calcular_costo_boletas, name='calcular_costo_boletas'),
]
