// Common Select2 configuration
$(document).ready(function() {
    const Select2Config = {
        defaultConfig: {
            width: '100%',
            theme: 'default',
            language: {
                noResults: function() { return "Nie znaleziono wyników"; },
                searching: function() { return "Szukam..."; }
            }
        },

        initWithPlaceholder: function(selector, placeholder, allowClear = true) {
            const config = {
                ...this.defaultConfig,
                placeholder: placeholder,
                allowClear: allowClear
            };
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
            if ($('#filter_id_projektu').length) {
                this.initWithPlaceholder('#filter_id_projektu', "Wszystkie projekty...");
            }
        }
    };

    Select2Config.initializeAll();
});