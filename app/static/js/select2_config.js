// Common Select2 configuration
// Define Select2Config globally
window.Select2Config = {
    defaultConfig: {
        width: '100%',
        theme: 'default',
        language: {
            noResults: function() { return "Nie znaleziono wyników"; },
            searching: function() { return "Szukam..."; }
        }
    },

    initWithPlaceholder: function(selector, placeholder, allowClear = true, dropdownParent = null) {
        const config = {
            ...this.defaultConfig,
            placeholder: placeholder,
            allowClear: allowClear
        };
        if (dropdownParent) {
            config.dropdownParent = dropdownParent;
        }
        $(selector).select2(config);
    },

    initializeSelect2WithTags: function(selector, ajaxUrl, placeholder) {
        $(selector).select2({
            ...this.defaultConfig,
            placeholder: placeholder,
            tags: true,
            tokenSeparators: [',', ' '],
            ajax: {
                url: ajaxUrl,
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return { q: params.term };
                },
                processResults: function (data) {
                    return { results: data.map(item => ({ id: item.text, text: item.text })) };
                },
                cache: true
            },
            createTag: function (params) {
                var term = $.trim(params.term);
                if (term === '') {
                    return null;
                }
                return {
                    id: term,
                    text: term,
                    newTag: true
                }
            }
        });
    },

    initializeAll: function() {
        // --- Inicjalizacje z oryginalnego pliku ---
        if ($('#specialties').length) {
            this.initWithPlaceholder('#specialties', "Wybierz specjalność - wpisz by filtrować");
        }
        if ($('#specjalnosci').length) {
            this.initWithPlaceholder('#specjalnosci', "Wybierz specjalności...");
        }
        if ($('#wojewodztwa').length) {
            this.initWithPlaceholder('#wojewodztwa', "Wybierz województwa...");
        }
        if ($('#powiaty').length) {
            this.initWithPlaceholder('#powiaty', "Wybierz powiaty...");
        }
        if ($('#firmy_select').length) {
                $('#firmy_select').select2({ ...this.defaultConfig, allowClear: false });
            }
        if ($('#id_firmy').length) {
            this.initWithPlaceholder('#id_firmy', "Wybierz firmę...", false);
        }
        if ($('#id_projektu').length) {
            this.initWithPlaceholder('#id_projektu', "Wybierz projekt...", false);
        }
        if ($('#filter_id_firmy').length) {
            this.initWithPlaceholder('#filter_id_firmy', "Wszystkie firmy...");
        }
        if ($('#filter_id_projektu').length) {
            this.initWithPlaceholder('#filter_id_projektu', "Wszystkie projekty...");
        }

        // --- Nowe inicjalizacje dla comboboxów ---
        if ($('#id_work_type_select').length) {
            this.initWithPlaceholder('#id_work_type_select', "Wybierz nazwę roboty...");
        }
        if ($('#id_kategorii_select').length) {
            this.initWithPlaceholder('#id_kategorii_select', "Wybierz kategorię...");
        }
        if ($('#id_oferty_select').length) {
            this.initWithPlaceholder('#id_oferty_select', "Wybierz ofertę...");
        }
        if ($('#filter_nazwa_roboty').length) {
            this.initWithPlaceholder('#filter_nazwa_roboty', "Wszystkie nazwy robót...");
        }
        if ($('#filter_kategoria').length) {
            this.initWithPlaceholder('#filter_kategoria', "Wszystkie kategorie...");
        }
        if ($('#filter_id_oferty').length) {
            this.initWithPlaceholder('#filter_id_oferty', "Wszystkie oferty...");
        }
        if ($('#filter_id_firmy').length) {
            this.initWithPlaceholder('#filter_id_firmy', "Wszystkie firmy...");
        }
        if ($('#work_type_category_select').length) {
            this.initWithPlaceholder('#work_type_category_select', 'Wybierz kategorię...', false)
        }
        if ($('#filter_id_projektu').length) {
            this.initWithPlaceholder('#filter_id_projektu', "Wszystkie projekty...");
        }
    }
};

$(document).ready(function() {
    window.Select2Config.initializeAll();

    // Listen for the custom event to update Select2 dropdowns
    $(document).on('itemAddedToSelect2', function(event, data) {
        var newItemId = data.id;
        var newItemName = data.name;
        var updateTargetSelector = data.updateTargetSelector;

        if (updateTargetSelector) {
            var $selectElement = $(updateTargetSelector);
            if ($selectElement.length) {
                // Destroy existing Select2 instance if it exists
                if ($selectElement.data('select2')) {
                    $selectElement.select2('destroy');
                }
                // Create a new option
                var newOption = new Option(newItemName, newItemId, true, true);
                // Append it to the select
                $selectElement.append(newOption);
                // Set the new item as selected and trigger change to update Select2
                $selectElement.val(newItemId).trigger('change');
                // Re-initialize Select2 on the element
                window.Select2Config.initWithPlaceholder($selectElement, $selectElement.data('placeholder') || 'Wybierz...', true);
            }
        }
    });
});