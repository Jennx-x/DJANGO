from django.db import models
from datetime import datetime

class BaseEvento(models.Model):
    """
    Clase abstracta que representa los atributos y métodos comunes
    para diferentes tipos de eventos.
    """
    _nombre = models.CharField(max_length=100)
    _fecha = models.DateTimeField()
    _lugar = models.CharField(max_length=200)

    # Propiedades públicas para acceder a los atributos privados
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        self._fecha = value

    @property
    def lugar(self):
        return self._lugar

    @lugar.setter
    def lugar(self, value):
        self._lugar = value

    def mostrar_info(self):
        """
        Método para mostrar información básica de un evento.
        """
        return f"Evento: {self._nombre}, Fecha: {self._fecha.strftime('%d/%m/%Y %H:%M')}, Lugar: {self._lugar}"

    @staticmethod
    def es_evento_proximo(fecha_evento):
        """
        Método estático para verificar si un evento es próximo
        (es decir, su fecha es mayor a la actual).
        """
        return fecha_evento > datetime.now()

    @classmethod
    def crear_evento(cls, nombre, fecha, lugar):
        """
        Método de clase para crear instancias de eventos.
        """
        return cls(_nombre=nombre, _fecha=fecha, _lugar=lugar)

    class Meta:
        abstract = True  # Declara la clase como abstracta


class Concierto(BaseEvento):
    """
    Modelo que representa un concierto, hereda de BaseEvento.
    """
    _artista = models.CharField(max_length=100)
    _duracion = models.PositiveIntegerField(help_text="Duración en minutos")
    
    # Campo adicional para identificar el tipo de evento
    tipo_evento = models.CharField(max_length=50, default='Concierto')

    # Propiedades públicas para acceder a los atributos privados
    @property
    def artista(self):
        return self._artista

    @artista.setter
    def artista(self, value):
        self._artista = value

    @property
    def duracion(self):
        return self._duracion

    @duracion.setter
    def duracion(self, value):
        self._duracion = value

    def mostrar_info(self):
        """
        Método sobrescrito para mostrar información específica de un concierto.
        """
        base_info = super().mostrar_info()  # Llama al método de la clase base
        return f"{base_info}, Artista: {self._artista}, Duración: {self._duracion} minutos"

    @staticmethod
    def calcular_costo_boletas(precio_base, cantidad_boletas):
        """
        Método estático para calcular el costo total de las boletas.
        """
        if cantidad_boletas < 1:
            raise ValueError("La cantidad de boletas debe ser al menos 1.")
        return precio_base * cantidad_boletas


class Conferencia(BaseEvento):
    """
    Modelo que representa una conferencia, hereda de BaseEvento.
    """
    _tema = models.CharField(max_length=200)
    _orador = models.CharField(max_length=100)
    
    # Campo adicional para identificar el tipo de evento
    tipo_evento = models.CharField(max_length=50, default='Conferencia')

    # Propiedades públicas para acceder a los atributos privados
    @property
    def tema(self):
        return self._tema

    @tema.setter
    def tema(self, value):
        self._tema = value

    @property
    def orador(self):
        return self._orador

    @orador.setter
    def orador(self, value):
        self._orador = value

    def mostrar_info(self):
        """
        Método sobrescrito para mostrar información específica de una conferencia.
        """
        base_info = super().mostrar_info()  # Llama al método de la clase base
        return f"{base_info}, Tema: {self._tema}, Orador: {self._orador}"

    @staticmethod
    def calcular_costo_boletas(precio_base, cantidad_boletas):
        """
        Método estático para calcular el costo total de las boletas.
        """
        if cantidad_boletas < 1:
            raise ValueError("La cantidad de boletas debe ser al menos 1.")
        return precio_base * cantidad_boletas
