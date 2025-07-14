

Problemy i błedy w konsoli przeglądarki:
1. Otwarcie strony /tenders/:
    - The Content Security Policy (CSP) prevents the evaluation of arbitrary strings as JavaScript to make it more difficult for an attacker to inject unathorized code on your site.

    To solve this issue, avoid using eval(), new Function(), setTimeout([string], ...) and setInterval([string], ...) for evaluating strings.

    If you absolutely must: you can enable string evaluation by adding unsafe-eval as an allowed source in a script-src directive.

    ⚠️ Allowing string evaluation comes at the risk of inline script injection.

    1 dyrektywa
    Lokalizacja źródła	Dyrektywa	Stan
    script-src	zablokowano
        - Incorrect use of <label for=FORM_ELEMENT>
    The label's for attribute refers to a form field by its name, not its id. This might prevent the browser from correctly autofilling the form and accessibility tools from working correctly.

    To fix this issue, refer to form fields by their id attribute.

    2 zasoby
    Label <label for="id_firmy" class="form-label">Firma</label>
    Label <label for="id_projektu" class="form-label">Projekt</label>

2. Otwarcie dowolnej oferty np /tenders/10:
    - The Content Security Policy (CSP) prevents the evaluation of arbitrary strings as JavaScript to make it more difficult for an attacker to inject unathorized code on your site.

    To solve this issue, avoid using eval(), new Function(), setTimeout([string], ...) and setInterval([string], ...) for evaluating strings.

    If you absolutely must: you can enable string evaluation by adding unsafe-eval as an allowed source in a script-src directive.

    ⚠️ Allowing string evaluation comes at the risk of inline script injection.

    1 dyrektywa
    Lokalizacja źródła	Dyrektywa	Stan
    script-src	zablokowano
 3. Twoarcie /tenders/new z formularzem dodawania nowej oferty:
    - The Content Security Policy (CSP) prevents the evaluation of arbitrary strings as JavaScript to make it more difficult for an attacker to inject unathorized code on your site.

    To solve this issue, avoid using eval(), new Function(), setTimeout([string], ...) and setInterval([string], ...) for evaluating strings.

    If you absolutely must: you can enable string evaluation by adding unsafe-eval as an allowed source in a script-src directive.

    ⚠️ Allowing string evaluation comes at the risk of inline script injection.

    1 dyrektywa
    Lokalizacja źródła	Dyrektywa	Stan
    script-src	zablokowano
        - Incorrect use of <label for=FORM_ELEMENT>
    The label's for attribute refers to a form field by its name, not its id. This might prevent the browser from correctly autofilling the form and accessibility tools from working correctly.

    To fix this issue, refer to form fields by their id attribute.

    1 zasób
    Label <label class="form-label" for="id_projektu">Projekt (opcjonalnie)</label>

4. Otwarcie modalu overlay na stronie /tenders/new do dodawania nowego projektu:
    - main.js:2 main.js loaded and ready!
    new:357 Uncaught ReferenceError: initializeSelect2 is not defined
        at HTMLDivElement.<anonymous> (new:357:17)
        at HTMLDivElement.<anonymous> (jquery-3.6.0.min.js:2:85239)
        at S.each (jquery-3.6.0.min.js:2:3003)
        at S.fn.init.each (jquery-3.6.0.min.js:2:1481)
        at Object.<anonymous> (jquery-3.6.0.min.js:2:85221)
        at c (jquery-3.6.0.min.js:2:28327)
        at Object.fireWith [as resolveWith] (jquery-3.6.0.min.js:2:29072)
        at l (jquery-3.6.0.min.js:2:79901)
        at XMLHttpRequest.<anonymous> (jquery-3.6.0.min.js:2:82355)
    (anonimowa) @ new:357
    (anonimowa) @ jquery-3.6.0.min.js:2
    each @ jquery-3.6.0.min.js:2
    each @ jquery-3.6.0.min.js:2
    (anonimowa) @ jquery-3.6.0.min.js:2
    c @ jquery-3.6.0.min.js:2
    fireWith @ jquery-3.6.0.min.js:2
    l @ jquery-3.6.0.min.js:2
    (anonimowa) @ jquery-3.6.0.min.js:2
    XMLHttpRequest.send
    send @ jquery-3.6.0.min.js:2
    ajax @ jquery-3.6.0.min.js:2
    S.fn.load @ jquery-3.6.0.min.js:2
    (anonimowa) @ new:355
    dispatch @ jquery-3.6.0.min.js:2
    v.handle @ jquery-3.6.0.min.js:2
    trigger @ jquery-3.6.0.min.js:2
    (anonimowa) @ jquery-3.6.0.min.js:2
    each @ jquery-3.6.0.min.js:2
    each @ jquery-3.6.0.min.js:2
    trigger @ jquery-3.6.0.min.js:2
    trigger @ event-handler.js:276
    show @ modal.js:101
    toggle @ modal.js:93
    (anonimowa) @ modal.js:366
    n @ event-handler.js:118
    new:191 Uncaught ReferenceError: initializeSelect2 is not defined
        at HTMLDivElement.<anonymous> (new:191:17)
        at HTMLDivElement.<anonymous> (jquery-3.6.0.min.js:2:85239)
        at S.each (jquery-3.6.0.min.js:2:3003)
        at S.fn.init.each (jquery-3.6.0.min.js:2:1481)
        at Object.<anonymous> (jquery-3.6.0.min.js:2:85221)
        at c (jquery-3.6.0.min.js:2:28327)
        at Object.fireWith [as resolveWith] (jquery-3.6.0.min.js:2:29072)
        at l (jquery-3.6.0.min.js:2:79901)
        at XMLHttpRequest.<anonymous> (jquery-3.6.0.min.js:2:82355)
    (anonimowa) @ new:191
    (anonimowa) @ jquery-3.6.0.min.js:2
    each @ jquery-3.6.0.min.js:2
    each @ jquery-3.6.0.min.js:2
    (anonimowa) @ jquery-3.6.0.min.js:2
    c @ jquery-3.6.0.min.js:2
    fireWith @ jquery-3.6.0.min.js:2
    l @ jquery-3.6.0.min.js:2
    (anonimowa) @ jquery-3.6.0.min.js:2
    XMLHttpRequest.send
    send @ jquery-3.6.0.min.js:2
    ajax @ jquery-3.6.0.min.js:2
    S.fn.load @ jquery-3.6.0.min.js:2
    (anonimowa) @ new:190
    dispatch @ jquery-3.6.0.min.js:2
    v.handle @ jquery-3.6.0.min.js:2
    - zamknięcie modalu rzyciskiem anuluj:
    new:1 Blocked aria-hidden on an element because its descendant retained focus. The focus must not be hidden from assistive technology users. Avoid using aria-hidden on a focused element or its ancestor. Consider using the inert attribute instead, which will also prevent focus. For more details, see the aria-hidden section of the WAI-ARIA specification at https://w3c.github.io/aria/#aria-hidden.
    Element with focus: <button.btn-close>
    Ancestor with aria-hidden: <div.modal fade#mainModal> <div class=​"modal fade" id=​"mainModal" tabindex=​"-1" style=​"display:​ block;​" aria-hidden=​"true">​…​</div>​

5. Na stronie /tenders/10/extract_data otwarcie modalu overlay do dodawania Nowej nazwy roboty:
    - main.js:2 main.js loaded and ready!
    extract_data:454 Uncaught ReferenceError: initializeSelect2 is not defined
        at HTMLDivElement.<anonymous> (extract_data:454:17)
        at HTMLDivElement.<anonymous> (jquery-3.6.0.min.js:2:85239)
        at S.each (jquery-3.6.0.min.js:2:3003)
        at S.fn.init.each (jquery-3.6.0.min.js:2:1481)
        at Object.<anonymous> (jquery-3.6.0.min.js:2:85221)
        at c (jquery-3.6.0.min.js:2:28327)
        at Object.fireWith [as resolveWith] (jquery-3.6.0.min.js:2:29072)
        at l (jquery-3.6.0.min.js:2:79901)
        at XMLHttpRequest.<anonymous> (jquery-3.6.0.min.js:2:82355)
    (anonimowa) @ extract_data:454
    (anonimowa) @ jquery-3.6.0.min.js:2
    each @ jquery-3.6.0.min.js:2
    each @ jquery-3.6.0.min.js:2
    (anonimowa) @ jquery-3.6.0.min.js:2
    c @ jquery-3.6.0.min.js:2
    fireWith @ jquery-3.6.0.min.js:2
    l @ jquery-3.6.0.min.js:2
    (anonimowa) @ jquery-3.6.0.min.js:2
    XMLHttpRequest.send
    send @ jquery-3.6.0.min.js:2
    ajax @ jquery-3.6.0.min.js:2
    S.fn.load @ jquery-3.6.0.min.js:2
    (anonimowa) @ extract_data:453
    dispatch @ jquery-3.6.0.min.js:2
    v.handle @ jquery-3.6.0.min.js:2
    - zamkniecie modalu za pomocą "x" bez wpisywania danyych:
    extract_data:1 Blocked aria-hidden on an element because its descendant retained focus. The focus must not be hidden from assistive technology users. Avoid using aria-hidden on a focused element or its ancestor. Consider using the inert attribute instead, which will also prevent focus. For more details, see the aria-hidden section of the WAI-ARIA specification at https://w3c.github.io/aria/#aria-hidden.
    Element with focus: <button.btn-close>
    Ancestor with aria-hidden: <div.modal fade#mainModal> <div class=​"modal fade" id=​"mainModal" tabindex=​"-1" style=​"display:​ block;​" aria-hidden=​"true">​…​</div>​

Miejsca w kodzie które moga powodować problemy:
1. Wielokrotne występowanie kodu js do obsługi modali overlay:
    - modal_form_handler.js w app/static/js/modal_form_handler.js
    - blok sripts w base.html
    - blok scripts w extract_helper.html
    - blok scripts w tender_form.html
    - blok scripts w unit_price_form.html
2. Wielekrotnbe występowanie kodu do inicjalizacji select2:
    - select2_config.js
    - bloki scripts na kodach róznych stron 
    
DO ANALIZY 
1. Strony do dodawania nowej firmy company_form.html i kompany_edit_form w połaczeniu z kodem javascript w pliku company_form.js dobrze radzą sobie z wyświetlaniam i przekazywaniem danych z modali - brak błedów w konsoli i na stronie - można  zaczerpnąć jako "dobry przykłąd"
   - 