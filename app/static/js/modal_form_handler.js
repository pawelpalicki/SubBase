$(document).ready(function() {
    // Obsługa modala dla dynamicznych formularzy (np. dodawanie projektu, kategorii)
    $('#mainModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Przycisk, który wywołał modal
        var url = button.data('url'); // Pobierz URL z atrybutu data-url
        var title = button.data('title'); // Pobierz tytuł z atrybutu data-title

        var modal = $(this);
        modal.find('.modal-title').text(title);
        modal.find('.modal-body').html('<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Ładowanie...</span></div></div>'); // Pokaż spinner ładowania

        // Załaduj zawartość formularza przez AJAX
        $.get(url, function(data) {
            modal.find('.modal-body').html(data);
            // Ponownie zainicjuj Select2, jeśli formularz go używa
            modal.find('select.select2-multiple').select2({
                dropdownParent: modal.find('.modal-body')
            });
            modal.find('select.select2-single').select2({
                dropdownParent: modal.find('.modal-body')
            });
        }).fail(function() {
            modal.find('.modal-body').html('<p class="text-danger">Nie udało się załadować formularza.</p>');
        });
    });

    // Obsługa wysyłania formularza wewnątrz modala
    $('#mainModal').on('submit', 'form', function(e) {
        e.preventDefault(); // Zapobiegaj domyślnej wysyłce formularza

        var form = $(this);
        var url = form.attr('action') || $('#mainModal').data('url'); // Użyj action formularza lub data-url modala
        var method = form.attr('method') || 'POST';
        var formData = new FormData(form[0]); // Użyj FormData do obsługi plików i innych pól

        // Usuń poprzednie błędy walidacji
        form.find('.invalid-feedback').remove();
        form.find('.is-invalid').removeClass('is-invalid');

        $.ajax({
            url: url,
            method: method,
            data: formData,
            processData: false, // Ważne: nie przetwarzaj danych
            contentType: false, // Ważne: nie ustawiaj typu zawartości
            success: function(response) {
                if (response.success) {
                    // Zamknij modal
                    $('#mainModal').modal('hide');
                    // Wyświetl komunikat sukcesu
                    toastr.success('Operacja zakończona sukcesem!');

                    // Odśwież pole select w formularzu głównym, jeśli istnieje
                    var selectField = $('#id_projektu'); // ID pola select w głównym formularzu
                    if (selectField.length) {
                        // Zniszcz istniejącą instancję Select2
                        if (selectField.data('select2')) {
                            selectField.select2('destroy');
                        }
                        // Dodaj nową opcję
                        var newOption = new Option(response.name, response.id, true, true);
                        selectField.append(newOption);
                        // Ustaw nowo dodany element jako wybrany
                        selectField.val(response.id);
                        // Ponownie zainicjuj Select2
                        selectField.select2({
                            placeholder: "--- Brak projektu ---", // Ustaw placeholder
                            allowClear: true // Pozwól na wyczyszczenie wyboru
                        });
                        selectField.trigger('change'); // Wywołaj zdarzenie zmiany, aby Select2 odświeżył swój wygląd
                    }
                    // Możesz też odświeżyć inne pola Select2, jeśli są powiązane
                    // np. dla kategorii, typów robót itp.
                    var workTypeSelect = $('#id_work_type');
                    if (workTypeSelect.length && response.type === 'work_type') { // Przykład dla typu roboty
                        var newWorkTypeOption = new Option(response.name, response.id, true, true);
                        workTypeSelect.append(newWorkTypeOption).trigger('change');
                        workTypeSelect.val(response.id).trigger('change');
                    }
                    var categorySelect = $('#id_kategorii');
                    if (categorySelect.length && response.type === 'category') { // Przykład dla kategorii
                        var newCategoryOption = new Option(response.name, response.id, true, true);
                        categorySelect.append(newCategoryOption).trigger('change');
                        categorySelect.val(response.id).trigger('change');
                    }


                } else {
                    // Wyświetl błędy walidacji
                    if (response.errors) {
                        $.each(response.errors, function(field, messages) {
                            var input = form.find('[name="' + field + '"]');
                            if (input.length) {
                                input.addClass('is-invalid');
                                $.each(messages, function(i, message) {
                                    input.after('<div class="invalid-feedback">' + message + '</div>');
                                });
                            } else {
                                // Błędy globalne formularza (np. _form)
                                form.prepend('<div class="alert alert-danger">' + messages.join('<br>') + '</div>');
                            }
                        });
                    } else {
                        toastr.error('Wystąpił nieznany błąd podczas przetwarzania formularza.');
                    }
                }
            },
            error: function(jqXHR) {
                // Obsługa błędów HTTP (np. 400 Bad Request, 500 Internal Server Error)
                if (jqXHR.status >= 400 && jqXHR.status < 500) {
                    var errorData = jqXHR.responseJSON;
                    if (errorData && errorData.errors) {
                        $.each(errorData.errors, function(field, messages) {
                            var input = form.find('[name="' + field + '"]');
                            if (input.length) {
                                input.addClass('is-invalid');
                                $.each(messages, function(i, message) {
                                    input.after('<div class="invalid-feedback">' + message + '</div>');
                                });
                            }
                        });
                    } else {
                        toastr.error('Wystąpił błąd serwera: ' + (jqXHR.responseJSON && jqXHR.responseJSON.message ? jqXHR.responseJSON.message : jqXHR.statusText));
                    }
                } else {
                    toastr.error('Wystąpił błąd komunikacji z serwerem.');
                }
            }
        });
    });
});
