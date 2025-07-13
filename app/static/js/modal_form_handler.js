$(document).ready(function() {
    var mainModal = $('#mainModal');

    mainModal.on('show.bs.modal', function (event) {
        // Disable the main form's submit button when modal opens
        $('#submitMainFormBtn').prop('disabled', true);
        var modal = $(this);
        var button = $(event.relatedTarget); // This can be an empty jQuery object or undefined
        var url = ''; // Initialize url to an empty string
        var title = '';
        var updateTargetSelector = '';

        // Determine URL, title, and updateTargetSelector based on how the modal was opened
        if (button.length > 0) { // Modal opened by a button click
            url = button.data('url') || '';
            title = button.data('title') || '';
            updateTargetSelector = button.data('update-target') || '';

            // Add _partial=true only if it's not already there
            if (url && !url.includes('_partial=true')) {
                url = url + (url.includes('?') ? '&' : '?') + '_partial=true';
            } else if (!url) { // If url was initially empty, just add _partial=true
                url = '_partial=true';
            }

            modal.data('triggerElement', button); // Store the trigger element
            modal.data('url', url); // Store the URL for nested modal logic
            modal.data('update-target', updateTargetSelector);
            modal.find('.modal-title').text(title);

        } else { // Modal opened programmatically (e.g., after secondary modal closes)
            // Retrieve stored data from the modal itself
            url = modal.data('url') || '';
            title = modal.find('.modal-title').text() || ''; // Keep existing title
            updateTargetSelector = modal.data('update-target') || '';
        }

        // Always show loading spinner and load content
        modal.find('.modal-body').html('<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Ładowanie...</span></div></div>');

        // Use the determined URL for loading content
        if (url) {
            $.get(url, function(data) {
                modal.find('.modal-body').html(data);
                if (window.Select2Config) {
                modal.find('select.select2-enable').each(function() {
                    var $this = $(this);
                    // Destroy existing Select2 instance if it exists
                    if ($this.data('select2')) {
                        $this.select2('destroy');
                    }
                    // Initialize with dynamic dropdownParent
                    window.Select2Config.initWithPlaceholder(this, $this.data('placeholder') || 'Wybierz...', true, modal.find('.modal-body'));
                });

                // --- FIX: Set selected category if category_id is in URL --- 
                var categoryIdFromUrl = new URLSearchParams(url).get('category_id');
                var selectedCategoryId = modal.data('selectedCategoryId') || categoryIdFromUrl;
                
                if (selectedCategoryId) {
                    var categorySelect = modal.find('#work_type_category_select_modal');
                    console.log('categorySelect length:', categorySelect.length);
                    if (categorySelect.length) {
                        setTimeout(function() {
                            categorySelect.val(selectedCategoryId).trigger('change');
                            
                        }, 50); // Small delay to ensure Select2 is ready
                    }
                }
            }
            }).fail(function() {
                modal.find('.modal-body').html('<p class="text-danger">Nie udało się załadować formularza.</p>');
            });
        } else {
            modal.find('.modal-body').html('<p class="text-danger">Błąd: Brak URL do załadowania treści modala.</p>');
        }
    });

    mainModal.on('submit', 'form', function(e) {
        e.preventDefault(); 

        var form = $(this);
        var url = form.attr('action');
        var method = form.attr('method') || 'POST';
        var formData = new FormData(form[0]);

        form.find('.is-invalid').removeClass('is-invalid');
        form.find('.invalid-feedback').remove();
        form.find('.alert').remove();

        $.ajax({
            url: url,
            method: method,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response, textStatus, jqXHR) {
                // Special handling for login form
                if (url.includes('/login')) {
                    // For login, always reload the page on success (2xx status)
                    // This handles both successful redirects and cases where the login form
                    // is re-rendered with flashed messages (e.g., invalid credentials).
                    window.location.reload();
                    return; // Stop further processing for login form
                }

                // Original logic for other forms (expecting JSON response)
                if (response.success) {
                    mainModal.modal('hide');
                    var updateTargetSelector = mainModal.data('update-target');
                    $(document).trigger('itemAddedToSelect2', {
                        id: response.id,
                        name: response.name,
                        updateTargetSelector: updateTargetSelector
                    });
                } else {
                    // Handle validation errors or other non-successful JSON responses
                    if (response.errors) {
                        $.each(response.errors, function(field, messages) {
                            var input = form.find('[name="' + field + '"]');
                            input.addClass('is-invalid');
                            var errorContainer = $('<div class="invalid-feedback"></div>');
                            errorContainer.html(messages.join('<br>'));
                            input.after(errorContainer);
                        });
                    } else {
                        var generalError = response.message || 'Wystąpił nieznany błąd.';
                        form.prepend('<div class="alert alert-danger">' + generalError + '</div>');
                    }
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // Special handling for login form
                if (url.includes('/login')) {
                    // For login, if an actual HTTP error occurs (e.g., 500), display a generic message.
                    // Flask's login endpoint typically returns 200 OK with HTML for failed logins,
                    // which would be caught by the 'success' callback and trigger a reload.
                    var errorMessage = 'Wystąpił błąd komunikacji z serwerem podczas logowania. Spróbuj ponownie.';
                    form.prepend('<div class="alert alert-danger">' + errorMessage + '</div>');
                    return; // Stop further processing for login form
                }

                // Original logic for other forms
                var form = mainModal.find('form');
                if ((jqXHR.status === 400 || jqXHR.status === 422) && jqXHR.responseJSON) {
                    var errorData = jqXHR.responseJSON;
                    if (errorData && errorData.errors) {
                        $.each(errorData.errors, function(field, messages) {
                            var input = form.find('[name="' + field + '"]');
                            if (input.length) {
                                input.addClass('is-invalid');
                                var errorContainer = input.next('.invalid-feedback');
                                if (errorContainer.length === 0) {
                                    errorContainer = $('<div class="invalid-feedback"></div>');
                                    input.after(errorContainer);
                                }
                                errorContainer.html(messages.join('<br>'));
                            }
                        });
                    } else {
                        var generalError = (errorData && errorData.message) ? errorData.message : 'Wystąpił błąd walidacji.';
                        form.prepend('<div class="alert alert-danger">' + generalError + '</div>');
                    }
                } else {
                    var errorMessage = (jqXHR.responseJSON && jqXHR.responseJSON.message) ? jqXHR.responseJSON.message : 'Wystąpił błąd komunikacji z serwerem.';
                    form.prepend('<div class="alert alert-danger">' + errorMessage + '</div>');
                }
            }
        });
    });

    // --- FIX: Simplified focus management on modal hide ---
    mainModal.on('hide.bs.modal', function (e) {
        if (document.activeElement) {
            $(document.activeElement).blur(); // Remove focus from any element inside the modal
        }
        // Optionally, set focus to body or a known element outside the modal
        $('body').focus(); 
    });

    mainModal.on('hidden.bs.modal', function (e) {
        // Clear modal content and data after it's fully hidden
        $(this).find('.modal-body').html('');
        $(this).removeData('triggerElement');
        // Enable the main form's submit button when modal closes
        $('#submitMainFormBtn').prop('disabled', false);
    });
});