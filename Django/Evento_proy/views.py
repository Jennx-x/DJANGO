from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Concierto, Conferencia
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

def index(request):
    # Recuperas conciertos
    conciertos = Concierto.objects.all()

    # Recuperas conferencias
    conferencias = Conferencia.objects.all()

    # Usando el método sobrescrito para obtener la info de conciertos
    info_conciertos = [concierto.mostrar_info() for concierto in conciertos]

    # Usando el método sobrescrito para obtener la info de conferencias
    info_conferencias = [conferencia.mostrar_info() for conferencia in conferencias]

    return render(request, 'index.html', {
        'conciertos': conciertos,
        'conferencias': conferencias,
        'info_conciertos': info_conciertos,
        'info_conferencias': info_conferencias,
    })


@csrf_exempt
def crear_evento(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            fecha = request.POST.get('fecha')
            lugar = request.POST.get('lugar')
            artista = request.POST.get('artista')
            duracion = request.POST.get('duracion')
            tema = request.POST.get('tema')  # Solo para conferencia
            orador = request.POST.get('orador')  # Solo para conferencia

            # Verificar si los datos se están recibiendo correctamente
            print(f"Nombre: {nombre}")
            print(f"Fecha: {fecha}")
            print(f"Lugar: {lugar}")
            print(f"Artista: {artista}")
            print(f"Duración: {duracion}")
            print(f"Tema: {tema}")
            print(f"Orador: {orador}")

            if not fecha:
                return JsonResponse({'status': 'error', 'mensaje': 'La fecha es obligatoria.'}, status=400)

            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%dT%H:%M")
            except ValueError:
                return JsonResponse({'status': 'error', 'mensaje': 'Formato de fecha inválido.'}, status=400)

            if artista and duracion:
                # Si los datos de concierto son enviados, crea un concierto
                Concierto.objects.create(
                    _nombre=nombre,
                    _fecha=fecha,
                    _lugar=lugar,
                    _artista=artista,
                    _duracion=int(duracion)
                )
            elif tema and orador:
                # Si los datos de conferencia son enviados, crea una conferencia
                Conferencia.objects.create(
                    _nombre=nombre,
                    _fecha=fecha,
                    _lugar=lugar,
                    _tema=tema,
                    _orador=orador
                )
            else:
                return JsonResponse({'status': 'error', 'mensaje': 'Faltan datos para crear el evento.'}, status=400)

            return JsonResponse({'status': 'success', 'mensaje': 'Evento creado correctamente.'})

        except Exception as e:
            print(f"Error al guardar el evento: {e}")
            return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=400)
        
# -----------------------------------------------------------------------------------------------
@csrf_exempt
def editar_evento(request, evento_id):
    try:
        if request.method == 'POST':
            # Obtener datos del formulario
            tipo_evento = request.POST.get('tipo_evento')
            nombre = request.POST.get('nombre')
            fecha = request.POST.get('fecha')
            lugar = request.POST.get('lugar')
            artista = request.POST.get('artista')  # Solo para concierto
            duracion = request.POST.get('duracion')  # Solo para concierto
            tema = request.POST.get('tema')  # Solo para conferencia
            orador = request.POST.get('orador')  # Solo para conferencia

            # Logs para depuración
            print(f"ID del evento: {evento_id}")
            print(f"Tipo de evento: {tipo_evento}")
            print(f"Datos recibidos: {request.POST}")

            # Validaciones
            if not tipo_evento:
                return JsonResponse({'status': 'error', 'mensaje': 'El tipo de evento es obligatorio.'}, status=400)

            if not fecha:
                return JsonResponse({'status': 'error', 'mensaje': 'La fecha es obligatoria.'}, status=400)

            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%dT%H:%M")
            except ValueError:
                return JsonResponse({'status': 'error', 'mensaje': 'Formato de fecha inválido.'}, status=400)

            # Buscar y actualizar el evento según su tipo
            if tipo_evento == 'concierto':
                evento = Concierto.objects.get(id=evento_id)
                evento.nombre = nombre
                evento.fecha = fecha
                evento.lugar = lugar
                evento.artista = artista
                evento.duracion = int(duracion)
                evento.save()

            elif tipo_evento == 'conferencia':
                evento = Conferencia.objects.get(id=evento_id)
                evento.nombre = nombre
                evento.fecha = fecha
                evento.lugar = lugar
                evento.tema = tema
                evento.orador = orador
                evento.save()

            return JsonResponse({'status': 'success', 'mensaje': 'Evento actualizado correctamente.'})

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'mensaje': 'El evento no existe.'}, status=404)

    except Exception as e:
        print(f"Error al guardar los cambios: {e}")  # Imprimir el error en el servidor
        return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=500)


# ----------------------------------------------------------------------------------------------------------------
# Vista para obtener los detalles del evento
@csrf_exempt
def obtener_evento(request):
    if request.method == 'GET':
        evento_id = request.GET.get('id')
        tipo_evento = request.GET.get('tipo')

        if tipo_evento == 'concierto':
            evento = Concierto.objects.get(id=evento_id)
            data = {
                'nombre': evento.nombre,
                'fecha': evento.fecha.strftime('%Y-%m-%dT%H:%M'),
                'lugar': evento.lugar,
                'artista': evento.artista,
                'duracion': evento.duracion
            }
        elif tipo_evento == 'conferencia':
            evento = Conferencia.objects.get(id=evento_id)
            data = {
                'nombre': evento.nombre,
                'fecha': evento.fecha.strftime('%Y-%m-%dT%H:%M'),
                'lugar': evento.lugar,
                'tema': evento.tema,
                'orador': evento.orador
            }

        return JsonResponse({'status': 'success', 'data': data})

# ----------------------------------------------------------------------------------------------------------------

# Eliminar un evento
@csrf_exempt
def eliminar_evento(request):
    if request.method == 'POST':
        try:
            evento_id = request.POST.get('evento_id')
            tipo_evento = request.POST.get('tipo_evento')

            if tipo_evento == 'concierto':
                evento = get_object_or_404(Concierto, id=evento_id)
            elif tipo_evento == 'conferencia':
                evento = get_object_or_404(Conferencia, id=evento_id)
            else:
                return JsonResponse({'status': 'error', 'mensaje': 'Tipo de evento no válido.'}, status=400)

            evento.delete()
            return JsonResponse({'status': 'success', 'mensaje': 'Evento eliminado correctamente.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=400)

# --------------------------------------------------------------------------------------------------------------------

def calcular_costo_boletas(request):
    try:
        precio_base = float(request.POST.get('precio_base'))
        cantidad_boletas = int(request.POST.get('cantidad_boletas'))
        
        if cantidad_boletas < 1:
            return JsonResponse({'status': 'error', 'mensaje': 'La cantidad de boletas debe ser al menos 1.'}, status=400)
        
        costo_total = precio_base * cantidad_boletas
        return JsonResponse({'status': 'success', 'mensaje': 'Costo calculado exitosamente.', 'costo_total': costo_total})
    except Exception as e:
        return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=400)