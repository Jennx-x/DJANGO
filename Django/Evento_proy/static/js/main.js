(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show'); // Remueve la clase 'show' para ocultar el spinner
            }
        }, 1);
    };
    spinner(); // Llama a la función spinner para ejecutarla

    // Botón "Volver arriba"
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });

    // Toggler de la barra lateral
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false; // Previene el comportamiento predeterminado
    });

    // Editar evento
    $(document).on('click', '.btn-editar', function () {
        const id = $(this).closest('tr').data('id');  // Obtener el ID del evento

        // Hacer una solicitud AJAX GET para obtener los detalles del evento
        $.ajax({
            url: `/evento_detalle/${id}/`,  // URL para obtener los detalles
            method: 'GET',
            success: function (response) {
                // Llenar los campos del formulario con los datos del evento
                $('#editarIdEvento').val(response.id);
                $('#editarNombre').val(response.nombre);
                $('#editarFecha').val(response.fecha);
                $('#editarLugar').val(response.lugar);
                $('#editarTipo').val(response.tipo_evento);

                // Dependiendo del tipo de evento, mostrar detalles adicionales
                if (response.tipo_evento === 'concierto') {
                    $('#editarDetalleEvento').html(`
                        <div class="form-group">
                            <label for="editarArtista">Artista</label>
                            <input type="text" class="form-control" id="editarArtista" value="${response.artista}" required>
                        </div>
                        <div class="form-group">
                            <label for="editarDuracion">Duración (minutos)</label>
                            <input type="number" class="form-control" id="editarDuracion" value="${response.duracion}" required>
                        </div>
                    `);
                } else {
                    $('#editarDetalleEvento').html(`
                        <div class="form-group">
                            <label for="editarTema">Tema</label>
                            <input type="text" class="form-control" id="editarTema" value="${response.tema}" required>
                        </div>
                        <div class="form-group">
                            <label for="editarOrador">Orador</label>
                            <input type="text" class="form-control" id="editarOrador" value="${response.orador}" required>
                        </div>
                    `);
                }

                // Mostrar el modal de edición
                $('#editarEventoModal').modal('show');
            },
            error: function () {
                alert('Error al cargar los detalles del evento.');
            }
        });
    });

    // Guardar cambios del evento (POST)
    $('#formEditarEvento').submit(function (e) {
        e.preventDefault();  // Prevenir el envío normal del formulario

        const id = $('#editarIdEvento').val();
        const tipo = $('#editarTipo').val();
        const nombre = $('#editarNombre').val();
        const fecha = $('#editarFecha').val();
        const lugar = $('#editarLugar').val();
        let datosExtra = {};

        // Obtener los detalles adicionales dependiendo del tipo de evento
        if (tipo === 'concierto') {
            datosExtra = {
                artista: $('#editarArtista').val(),
                duracion: $('#editarDuracion').val()
            };
        } else {
            datosExtra = {
                tema: $('#editarTema').val(),
                orador: $('#editarOrador').val()
            };
        }

        // Enviar los datos mediante AJAX
        $.ajax({
            url: `/editar_evento/${id}/`,  // URL para editar el evento
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'nombre': nombre,
                'fecha': fecha,
                'lugar': lugar,
                'tipo_evento': tipo,
                ...datosExtra
            },
            success: function (response) {
                if (response.success) {
                    // Si la actualización fue exitosa, actualizamos la tabla
                    const eventoActualizado = response.evento;
                    const fila = $(`tr[data-id='${eventoActualizado.id}']`);

                    // Actualizamos los valores de la fila
                    fila.find('td:nth-child(1)').text(eventoActualizado.nombre);
                    fila.find('td:nth-child(2)').text(eventoActualizado.fecha);
                    fila.find('td:nth-child(3)').text(eventoActualizado.lugar);
                    fila.find('td:nth-child(4)').text(eventoActualizado.artista || eventoActualizado.tema);
                    fila.find('td:nth-child(5)').text(eventoActualizado.duracion || eventoActualizado.orador);

                    // Cerrar el modal
                    $('#editarEventoModal').modal('hide');
                } else {
                    alert('Error al guardar los cambios.');
                }
            },
            error: function () {
                alert('Error al procesar la solicitud.');
            }
        });
    });

    // Eliminar evento
    $(document).on('click', '.btn-eliminar', function () {
        const id = $(this).closest('tr').data('id');  // Obtener el ID del evento

        // Mostrar el modal de confirmación de eliminación
        $('#confirmarEliminacion').modal('show');

        // Al hacer clic en eliminar, eliminar el evento
        $('#confirmarEliminarBtn').click(function () {
            $.ajax({
                url: `/eliminar_evento/${id}/`,
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function (response) {
                    if (response.success) {
                        // Eliminar la fila de la tabla
                        $(`tr[data-id='${id}']`).remove();
                        $('#confirmarEliminacion').modal('hide');
                    } else {
                        alert('Error al eliminar el evento.');
                    }
                },
                error: function () {
                    alert('Error al procesar la solicitud de eliminación.');
                }
            });
        });
    });

})(jQuery);
