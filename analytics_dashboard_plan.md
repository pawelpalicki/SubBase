# Plan Rozwoju: Pulpit Analityczny Cen

Niniejszy dokument opisuje plan implementacji nowego modułu analitycznego w aplikacji SubBase.

## Wizja

Stworzenie interaktywnego pulpitu analitycznego, który po wyborze konkretnego **rodzaju roboty** (np. "Wykopy pod fundamenty") dynamicznie zaprezentuje użytkownikowi kluczowe analizy w formie czytelnych widżetów.

---

## Plan Implementacji

### Krok 1: Stworzenie Podstaw Nowej Strony
- Utworzenie nowej trasy w `app/tenders/routes.py` pod adresem `/tenders/analysis_dashboard`.
- Stworzenie nowego pliku szablonu `app/tenders/templates/analysis_dashboard.html`.
- Dodanie linku do nowej strony w głównym menu nawigacyjnym (w `base.html`), np. pod nazwą "Pulpit Analityczny".

### Krok 2: Główny Element Interaktywny - Wybór Rodzaju Roboty
- Umieszczenie na górze nowej strony listy rozwijanej, która pozwoli użytkownikowi wybrać jeden, konkretny **rodzaj roboty** (`WorkType`) do analizy.

### Krok 3: Implementacja Widżetów Analitycznych
Po wybraniu rodzaju roboty, strona dynamicznie załaduje następujące widżety:

1.  **Widżet 1: Kluczowe Statystyki**
    -   **Cena Minimalna:** Najniższa znaleziona cena.
    -   **Cena Maksymalna:** Najwyższa znaleziona cena.
    -   **Cena Średnia:** Średnia arytmetyczna.
    -   **Mediana Cen:** Środkowa wartość ceny.
    -   **Liczba Ofert:** Liczba ofert uwzględnionych w analizie.

2.  **Widżet 2: Wykres Liniowy - Ewolucja Ceny w Czasie**
    -   Wykres pokazujący, jak średnia cena dla danej roboty zmieniała się w poszczególnych miesiącach/kwartałach.

3.  **Widżet 3: Wykres Słupkowy - Porównanie Cen wg Wykonawcy**
    -   Wykres pokazujący średnią cenę oferowaną przez każdą z firm dla wybranej roboty.

4.  **Widżet 4: Tabela z Danymi Źródłowymi**
    -   Tabela prezentująca wszystkie konkretne pozycje cenowe, na podstawie których powstały analizy, zapewniając pełną transparentność.

### Krok 4: Stworzenie Endpoints API do Zasilania Wykresów
- Stworzenie w `routes.py` pomocniczych tras (API), które będą zwracać dane w formacie JSON na potrzeby wykresów (np. `/api/price_trend/<work_type_id>`).
- Wykorzystanie biblioteki JavaScript (np. Chart.js) do renderowania wykresów po stronie klienta.

WDRAŻANIE:
Zgodnie z planem, zaczynam Krok 1: Stworzenie Podstaw Nowej Strony.

  Najpierw dodam link do "Pulpitu Analitycznego" w menu nawigacyjnym, modyfikując plik app/templates/base.html. Umieszczę go w rozwijanym menu "Ceny
  Jednostkowe".
 ╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/templates/base.html:                         <li><a... =>                         <li><a...                                           │
 │                                                                                                                                                   │
 │    Error: Failed to edit, could not find the string to replace.                                                                                   │
 ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Wygląda na to, że poprzednia próba modyfikacji pliku base.html nie powiodła się, ponieważ nie znalazłem dokładnego tekstu. Prawdopodobnie jest tam
  jakaś subtelna różnica w białych znakach.

  Odczytam plik base.html, aby uzyskać jego dokładną zawartość i upewnić się, że tym razem modyfikacja się powiedzie.
 ╭──────────────────────────────────────╮
 │ ✔  ReadFile app/templates/base.html  │
 ╰──────────────────────────────────────╯
✦ Dziękuję. Teraz widzę dokładną strukturę menu. Rzeczywiście, nazwa menu to "Analizy", a nie "Ceny Jednostkowe".

  Poprawiam swoją strategię i dodam link do "Pulpitu Analitycznego" w menu "Analizy".
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/templates/base.html:                         <ul cl... =>                         <ul cl...                                     │
 │                                                                                                                                             │
 │    63             <ul class="dropdown-menu" aria-labelledby="analysisDropdown">                                                             │
 │    64                 <li><a class="dropdown-item" href="{{ url_for('tenders.unit_prices_analysis') }}">Porównanie cen                      │
 │           jednostkowych</a></li>                                                                                                            │
 │    65                 <li><a class="dropdown-item" href="{{ url_for('tenders.list_all_unit_prices') }}">Wszystkie ceny                      │
 │           jednostkowe</a></li>                                                                                                              │
 │    66   +             <li><hr class="dropdown-divider"></li>                                                                                │
 │    67   +             <li><a class="dropdown-item" href="{{ url_for('tenders.analysis_dashboard') }}">Pulpit Analityczny</a></li>           │
 │    68             </ul>                                                                                                                     │
 │    69         </li>                                                                                                                         │
 │    70     </ul>                                                                                                                             │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Link w menu został dodany.

  Teraz dodam nową trasę analysis_dashboard do pliku app/tenders/routes.py. Na razie będzie ona tylko renderować pusty szablon.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/tenders/routes.py:     return redirect (url_for('... =>     return redirect (url_for('...                                       │
 │                                                                                                                                             │
 │    Error: Failed to edit, could not find the string to replace.                                                                             │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Znowu napotkałem problem z dokładnym dopasowaniem tekstu. To się zdarza, gdy plik jest dynamiczny.

  Ponownie odczytam plik app/tenders/routes.py, aby upewnić się, że mam jego najnowszą wersję, a następnie dodam nową trasę w odpowiednim miejscu.
 ╭────────────────────────────────────╮
 │ ✔  ReadFile app/tenders/routes.py  │
 ╰────────────────────────────────────╯
✦ Dziękuję. Mam aktualną zawartość pliku. Teraz dodam nową trasę na końcu pliku.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/tenders/routes.py:     price = UnitPrice.query.ge... =>     price = UnitPrice.query.ge...                                       │
 │                                                                                                                                             │
 │    598        db.session.commit()                                                                                                           │
 │    599        flash('Pozycja cenowa została usunięta.', 'success')                                                                          │
 │    600        return redirect(url_for('tenders.tender_details', tender_id=tender_id))                                                       │
 │    601  +                                                                                                                                   │
 │    602  + @tenders_bp.route('/analysis_dashboard')                                                                                          │
 │    603  + @login_required                                                                                                                   │
 │    604  + def analysis_dashboard():                                                                                                         │
 │    605  +     """                                                                                                                           │
 │    606  +     Wyświetla pulpit analityczny do interaktywnej analizy cen jednostkowych.                                                      │
 │    607  +     """                                                                                                                           │
 │    608  +     # Na razie tylko renderujemy szablon, dane będą ładowane dynamicznie                                                          │
 │    609  +     return render_template('analysis_dashboard.html', title='Pulpit Analityczny Cen')                                             │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Trasa została dodana.

  Na koniec tworzę nowy, pusty na razie plik szablonu analysis_dashboard.html. Będzie on stanowił bazę dla naszego pulpitu analitycznego.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  WriteFile Writing to ...app/templates/analysis_dashboard.html                                                                            │
 │                                                                                                                                             │
 │     1 {% extends "base.html" %}                                                                                                             │
 │     2                                                                                                                                       │
 │     3 {% block content %}                                                                                                                   │
 │     4 <div class="container mt-4">                                                                                                          │
 │     5     <div class="card">                                                                                                                │
 │     6         <div class="card-header">                                                                                                     │
 │     7             <h2>{{ title }}</h2>                                                                                                      │
 │     8         </div>                                                                                                                        │
 │     9         <div class="card-body">                                                                                                       │
 │    10             <p>Pulpit analityczny jest w budowie. Wkrótce pojawią się tu interaktywne wykresy i analizy.</p>                          │
 │    11             <p>Proszę wybrać rodzaj roboty, aby rozpocząć analizę.</p>                                                                │
 │    12         </div>                                                                                                                        │
 │    13     </div>                                                                                                                            │
 │    14 </div>                                                                                                                                │
 │    15 {% endblock %}                                                                                                                        │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Zakończyłem Krok 1. Stworzyłem podstawy dla nowej strony "Pulpit Analityczny Cen". Dodałem link w menu, utworzyłem trasę w logice aplikacji oraz
  przygotowałem plik szablonu.

  Teraz przechodzę do Kroku 2: Implementacja głównego elementu interaktywnego, czyli listy rozwijanej do wyboru rodzaju roboty.

  Zmodyfikuję plik analysis_dashboard.html, aby zawierał formularz z listą rozwijaną. Dodatkowo, w pliku routes.py przekażę do szablonu listę
  wszystkich dostępnych rodzajów robót, aby wypełnić tę listę.

  Zaczynam od modyfikacji routes.py.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/tenders/routes.py: @tenders_bp.route('/analysis_d... => @tenders_bp.route('/analysis_d...                                       │
 │                                                                                                                                             │
 │    605    """                                                                                                                               │
 │    606    Wyświetla pulpit analityczny do interaktywnej analizy cen jednostkowych.                                                          │
 │    607    """                                                                                                                               │
 │    608  - # Na razie tylko renderujemy szablon, dane będą ładowane dynamicznie                                                              │
 │    609  - return render_template('analysis_dashboard.html', title='Pulpit Analityczny Cen')                                                 │
 │    608  + work_types = WorkType.query.order_by(WorkType.name).all()                                                                         │
 │    609  + return render_template('analysis_dashboard.html',                                                                                 │
 │    610  +                        title='Pulpit Analityczny Cen',                                                                            │
 │    611  +                        work_types=work_types)                                                                                     │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Logika trasy została zaktualizowana.

  Teraz dodam formularz z listą rozwijaną do pliku analysis_dashboard.html. Po wybraniu rodzaju roboty i kliknięciu przycisku, strona przeładuje się,
  przekazując wybrane ID w adresie URL, co pozwoli nam w kolejnym kroku załadować odpowiednie dane.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit ...app/templates/analysis_dashboard.html: {% extends "base.html" %}... => {% extends "base.html" %}...                              │
 │                                                                                                                                             │
 │    7                  <h2>{{ title }}</h2>                                                                                                  │
 │    8              </div>                                                                                                                    │
 │    9              <div class="card-body">                                                                                                   │
 │    10   -             <p>Pulpit analityczny jest w budowie. Wkrótce pojawią się tu interaktywne wykresy i analizy.</p>                      │
 │    11   -             <p>Proszę wybrać rodzaj roboty, aby rozpocząć analizę.</p>                                                            │
 │    10   +             <form method="GET" action="{{ url_for('tenders.analysis_dashboard') }}">                                              │
 │    11   +                 <div class="row align-items-end">                                                                                 │
 │    12   +                     <div class="col-md-8">                                                                                        │
 │    13   +                         <label for="work_type_id" class="form-label"><strong>Wybierz rodzaj roboty do analizy:</strong></label>   │
 │    14   +                         <select name="work_type_id" id="work_type_id" class="form-select select2-enable">                         │
 │    15   +                             <option value="">-- Wybierz z listy --</option>                                                       │
 │    16   +                             {% for wt in work_types %}                                                                            │
 │    17   +                                 <option value="{{ wt.id }}" {% if selected_work_type_id == wt.id %}selected{% endif %}>{{         │
 │           wt.name }}</option>                                                                                                               │
 │    18   +                             {% endfor %}                                                                                          │
 │    19   +                         </select>                                                                                                 │
 │    20                         </div>                                                                                                        │
 │    21   +                     <div class="col-md-4">                                                                                        │
 │    22   +                         <button type="submit" class="btn btn-primary w-100">Analizuj</button>                                     │
 │    23                         </div>                                                                                                        │
 │    24                     </div>                                                                                                            │
 │    25   +             </form>                                                                                                               │
 │    26   +         </div>                                                                                                                    │
 │    27   +     </div>                                                                                                                        │
 │    28   +                                                                                                                                   │
 │    29   +     {% if selected_work_type_id %}                                                                                                │
 │    30   +     <div id="analysis-results" class="mt-4">                                                                                      │
 │    31   +         <p class="text-center">Wyniki analizy dla wybranego rodzaju roboty pojawią się tutaj.</p>                                 │
 │    32   +         <!-- W kolejnych krokach tutaj będą ładowane widżety -->                                                                  │
 │    33   +     </div>                                                                                                                        │
 │    34   +     {% endif %}                                                                                                                   │
 │    35   + </div>                                                                                                                            │
 │    36     {% endblock %}                                                                                                                    │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Zakończyłem Krok 2. Strona "Pulpit Analityczny Cen" zawiera teraz listę rozwijaną, która pozwala wybrać rodzaj roboty do analizy.

  Teraz muszę jeszcze zaktualizować logikę trasy, aby odczytywała wybrany work_type_id z adresu URL.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/tenders/routes.py: @tenders_bp.route('/analysis_d... => @tenders_bp.route('/analysis_d...                                       │
 │                                                                                                                                             │
 │    606    Wyświetla pulpit analityczny do interaktywnej analizy cen jednostkowych.                                                          │
 │    607    """                                                                                                                               │
 │    608    work_types = WorkType.query.order_by(WorkType.name).all()                                                                         │
 │    609  + selected_work_type_id = request.args.get('work_type_id', type=int)                                                                │
 │    610  +                                                                                                                                   │
 │    611    return render_template('analysis_dashboard.html',                                                                                 │
 │    612                           title='Pulpit Analityczny Cen',                                                                            │
 │    611  -                        work_types=work_types)                                                                                     │
 │    613  +                        work_types=work_types,                                                                                     │
 │    614  +                        selected_work_type_id=selected_work_type_id)                                                               │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Gotowe. Podstawowa interaktywność jest już zaimplementowana.

  Przechodzę do Kroku 3: Implementacja widżetów analitycznych. Zacznę od Widżetu 1: Kluczowe Statystyki.

  Zmodyfikuję trasę analysis_dashboard tak, aby po wybraniu rodzaju roboty, obliczała kluczowe statystyki (min, max, średnia, mediana, liczba ofert)
  i przekazywała je do szablonu. Następnie wyświetlę te statystyki w nowo utworzonym kontenerze na wyniki analizy.

  Zaczynam od aktualizacji routes.py.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/tenders/routes.py: from flask import Blueprint, r... => from datetime import datetime...                                        │
 │                                                                                                                                             │
 │    1    + from datetime import datetime                                                                                                     │
 │    2    + from statistics import median                                                                                                     │
 │    3      from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, jsonify,       │
 │           send_file                                                                                                                         │
 │    4      from flask_login import login_required                                                                                            │
 │    5      from app import db                                                                                                                │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Teraz dodam logikę obliczania statystyk.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/tenders/routes.py: @tenders_bp.route('/analysis_d... => @tenders_bp.route('/analysis_d...                                       │
 │                                                                                                                                             │
 │    610    work_types = WorkType.query.order_by(WorkType.name).all()                                                                         │
 │    611    selected_work_type_id = request.args.get('work_type_id', type=int)                                                                │
 │    612                                                                                                                                      │
 │    613  + stats = {}                                                                                                                        │
 │    614  + if selected_work_type_id:                                                                                                         │
 │    615  +     prices = db.session.query(UnitPrice.cena_jednostkowa).filter(UnitPrice.id_work_type == selected_work_type_id).all()           │
 │    616  +     price_values = [float(p[0]) for p in prices]                                                                                  │
 │    617  +                                                                                                                                   │
 │    618  +     if price_values:                                                                                                              │
 │    619  +         stats = {                                                                                                                 │
 │    620  +             'min_price': min(price_values),                                                                                       │
 │    621  +             'max_price': max(price_values),                                                                                       │
 │    622  +             'avg_price': sum(price_values) / len(price_values),                                                                   │
 │    623  +             'median_price': median(price_values),                                                                                 │
 │    624  +             'offer_count': len(price_values)                                                                                      │
 │    625  +         }                                                                                                                         │
 │    626  +                                                                                                                                   │
 │    627    return render_template('analysis_dashboard.html',                                                                                 │
 │    628                           title='Pulpit Analityczny Cen',                                                                            │
 │    629                           work_types=work_types,                                                                                     │
 │    616  -                        selected_work_type_id=selected_work_type_id)                                                               │
 │    ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════  │
 │    630  +                        selected_work_type_id=selected_work_type_id,                                                               │
 │    631  +                        stats=stats)                                                                                               │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Logika po stronie serwera jest gotowa.

  Teraz wyświetlę te statystyki w pliku analysis_dashboard.html. Dodam nową sekcję, która pojawi się tylko wtedy, gdy statystyki zostaną obliczone.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit ...app/templates/analysis_dashboard.html:     {% if selected_work_type_i... =>     {% if selected_work_type_i...                    │
 │                                                                                                                                             │
 │    28                                                                                                                                       │
 │    29     {% if selected_work_type_id %}                                                                                                    │
 │    30     <div id="analysis-results" class="mt-4">                                                                                          │
 │    31   -     <p class="text-center">Wyniki analizy dla wybranego rodzaju roboty pojawią się tutaj.</p>                                     │
 │    31   +     {% if stats %}                                                                                                                │
 │    32   +     <div class="row">                                                                                                             │
 │    33   +         <div class="col-md-12">                                                                                                   │
 │    34   +             <div class="card">                                                                                                    │
 │    35   +                 <div class="card-header">                                                                                         │
 │    36   +                     <h4 class="card-title">Kluczowe Statystyki</h4>                                                               │
 │    37   +                 </div>                                                                                                            │
 │    38   +                 <div class="card-body">                                                                                           │
 │    39   +                     <div class="row text-center">                                                                                 │
 │    40   +                         <div class="col">                                                                                         │
 │    41   +                             <div class="stat-box p-3 border rounded">                                                             │
 │    42   +                                 <h5 class="stat-title">Cena Minimalna</h5>                                                        │
 │    43   +                                 <p class="stat-value fs-4">{{ "%.2f"|format(stats.min_price) }} zł</p>                            │
 │    44   +                             </div>                                                                                                │
 │    45   +                         </div>                                                                                                    │
 │    46   +                         <div class="col">                                                                                         │
 │    47   +                             <div class="stat-box p-3 border rounded">                                                             │
 │    48   +                                 <h5 class="stat-title">Cena Maksymalna</h5>                                                       │
 │    49   +                                 <p class="stat-value fs-4">{{ "%.2f"|format(stats.max_price) }} zł</p>                            │
 │    50   +                             </div>                                                                                                │
 │    51   +                         </div>                                                                                                    │
 │    52   +                         <div class="col">                                                                                         │
 │    53   +                             <div class="stat-box p-3 border rounded">                                                             │
 │    54   +                                 <h5 class="stat-title">Cena Średnia</h5>                                                          │
 │    55   +                                 <p class="stat-value fs-4">{{ "%.2f"|format(stats.avg_price) }} zł</p>                            │
 │    56   +                             </div>                                                                                                │
 │    57   +                         </div>                                                                                                    │
 │    58   +                         <div class="col">                                                                                         │
 │    59   +                             <div class="stat-box p-3 border rounded">                                                             │
 │    60   +                                 <h5 class="stat-title">Mediana Cen</h5>                                                           │
 │    61   +                                 <p class="stat-value fs-4">{{ "%.2f"|format(stats.median_price) }} zł</p>                         │
 │    62   +                             </div>                                                                                                │
 │    63   +                         </div>                                                                                                    │
 │    64   +                         <div class="col">                                                                                         │
 │    65   +                             <div class="stat-box p-3 border rounded">                                                             │
 │    66   +                                 <h5 class="stat-title">Liczba Ofert</h5>                                                          │
 │    67   +                                 <p class="stat-value fs-4">{{ stats.offer_count }}</p>                                            │
 │    68   +                             </div>                                                                                                │
 │    69   +                         </div>                                                                                                    │
 │    70   +                     </div>                                                                                                        │
 │    71   +                 </div>                                                                                                            │
 │    72   +             </div>                                                                                                                │
 │    73   +         </div>                                                                                                                    │
 │    74   +     </div>                                                                                                                        │
 │    75   +     {% else %}                                                                                                                    │
 │    76   +     <div class="alert alert-info mt-4">Brak danych cenowych dla wybranego rodzaju roboty.</div>                                   │
 │    77   +     {% endif %}                                                                                                                   │
 │    78         <!-- W kolejnych krokach tutaj będą ładowane widżety -->                                                                      │
 │    79     </div>                                                                                                                            │
 │    80     {% endif %}                                                                                                                       │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Zakończyłem implementację Widżetu 1: Kluczowe Statystyki.

  Teraz, po wybraniu rodzaju roboty i kliknięciu "Analizuj", pod formularzem powinna pojawić się sekcja z podstawowymi statystykami cenowymi.

  Przechodzę do implementacji Widżetu 2: Wykres Liniowy - Ewolucja Ceny w Czasie.

  Wymaga to stworzenia nowego endpointu API, który będzie zwracał dane do wykresu, oraz dodania kodu JavaScript, który ten wykres wygeneruje.

  Najpierw stworzę endpoint API w routes.py.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/tenders/routes.py:                            sel... =>                            sel...                                       │
 │                                                                                                                                             │
 │    629                               work_types=work_types,                                                                                 │
 │    630                               selected_work_type_id=selected_work_type_id,                                                           │
 │    631                               stats=stats)                                                                                           │
 │    632  +                                                                                                                                   │
 │    633  + @tenders_bp.route('/api/price_evolution/<int:work_type_id>')                                                                      │
 │    634  + @login_required                                                                                                                   │
 │    635  + def price_evolution_data(work_type_id):                                                                                           │
 │    636  +     """                                                                                                                           │
 │    637  +     Zwraca dane do wykresu ewolucji ceny w czasie dla danego rodzaju roboty.                                                      │
 │    638  +     """                                                                                                                           │
 │    639  +     data = db.session.query(                                                                                                      │
 │    640  +         func.to_char(Tender.data_otrzymania, 'YYYY-MM'),                                                                          │
 │    641  +         func.avg(UnitPrice.cena_jednostkowa)                                                                                      │
 │    642  +     ).join(Tender, UnitPrice.id_oferty == Tender.id)\                                                                             │
 │    643  +      .filter(UnitPrice.id_work_type == work_type_id)\                                                                             │
 │    644  +      .group_by(func.to_char(Tender.data_otrzymania, 'YYYY-MM'))\                                                                  │
 │    645  +      .order_by(func.to_char(Tender.data_otrzymania, 'YYYY-MM'))\                                                                  │
 │    646  +      .all()                                                                                                                       │
 │    647  +                                                                                                                                   │
 │    648  +     labels = [row[0] for row in data]                                                                                             │
 │    649  +     values = [float(row[1]) for row in data]                                                                                      │
 │    650  +                                                                                                                                   │
 │    651  +     return jsonify({'labels': labels, 'values': values})                                                                          │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Endpoint API został utworzony.

  Teraz dodam w szablonie analysis_dashboard.html element <canvas> dla wykresu oraz kod JavaScript, który pobierze dane z nowo utworzonego endpointu
  i wygeneruje wykres liniowy za pomocą biblioteki Chart.js.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit ...app/templates/analysis_dashboard.html:         {% else %}... =>         <div class="row mt-4">...                                │
 │                                                                                                                                             │
 │    72                     </div>                                                                                                            │
 │    73                 </div>                                                                                                                │
 │    74             </div>                                                                                                                    │
 │    75   +         <div class="row mt-4">                                                                                                    │
 │    76   +             <div class="col-md-12">                                                                                               │
 │    77   +                 <div class="card">                                                                                                │
 │    78   +                     <div class="card-header">                                                                                     │
 │    79   +                         <h4 class="card-title">Ewolucja Ceny w Czasie</h4>                                                        │
 │    80   +                     </div>                                                                                                        │
 │    81   +                     <div class="card-body">                                                                                       │
 │    82   +                         <canvas id="priceEvolutionChart"></canvas>                                                                │
 │    83   +                     </div>                                                                                                        │
 │    84   +                 </div>                                                                                                            │
 │    85   +             </div>                                                                                                                │
 │    86   +         </div>                                                                                                                    │
 │    87             {% else %}                                                                                                                │
 │    88             <div class="alert alert-info mt-4">Brak danych cenowych dla wybranego rodzaju roboty.</div>                               │
 │    89             {% endif %}                                                                                                               │
 │    92         {% endif %}                                                                                                                   │
 │    93     </div>                                                                                                                            │
 │    94     {% endblock %}                                                                                                                    │
 │    95   +                                                                                                                                   │
 │    96   + {% block scripts %}                                                                                                               │
 │    97   + {{ super() }}                                                                                                                     │
 │    98   + <script>                                                                                                                          │
 │    99   + $(document).ready(function() {                                                                                                    │
 │    100  +     // Inicjalizacja Select2                                                                                                      │
 │    101  +     $('.select2-enable').select2({                                                                                                │
 │    102  +         placeholder: "-- Wybierz z listy --",                                                                                     │
 │    103  +         allowClear: true                                                                                                          │
 │    104  +     });                                                                                                                           │
 │    105  +                                                                                                                                   │
 │    106  +     {% if selected_work_type_id and stats %}                                                                                      │
 │    107  +     // Wykres Ewolucji Ceny                                                                                                       │
 │    108  +     $.ajax({                                                                                                                      │
 │    109  +         url: `/tenders/api/price_evolution/{{ selected_work_type_id }}`,                                                          │
 │    110  +         success: function(data) {                                                                                                 │
 │    111  +             const ctx = document.getElementById('priceEvolutionChart').getContext('2d');                                          │
 │    112  +             new Chart(ctx, {                                                                                                      │
 │    113  +                 type: 'line',                                                                                                     │
 │    114  +                 data: {                                                                                                           │
 │    115  +                     labels: data.labels,                                                                                          │
 │    116  +                     datasets: [{                                                                                                  │
 │    117  +                         label: 'Średnia cena',                                                                                    │
 │    118  +                         data: data.values,                                                                                        │
 │    119  +                         borderColor: 'rgba(75, 192, 192, 1)',                                                                     │
 │    120  +                         backgroundColor: 'rgba(75, 192, 192, 0.2)',                                                               │
 │    121  +                         fill: true,                                                                                               │
 │    122  +                         tension: 0.1                                                                                              │
 │    123  +                     }]                                                                                                            │
 │    124  +                 },                                                                                                                │
 │    125  +                 options: {                                                                                                        │
 │    126  +                     scales: {                                                                                                     │
 │    127  +                         y: {                                                                                                      │
 │    128  +                             beginAtZero: false,                                                                                   │
 │    129  +                             ticks: {                                                                                              │
 │    130  +                                 callback: function(value, index, values) {                                                        │
 │    131  +                                     return value.toFixed(2) + ' zł';                                                              │
 │    132  +                                 }                                                                                                 │
 │    133  +                             }                                                                                                     │
 │    134  +                         }                                                                                                         │
 │    135  +                     },                                                                                                            │
 │    136  +                     plugins: {                                                                                                    │
 │    137  +                         tooltip: {                                                                                                │
 │    138  +                             callbacks: {                                                                                          │
 │    139  +                                 label: function(context) {                                                                        │
 │    140  +                                     let label = context.dataset.label || '';                                                      │
 │    141  +                                     if (label) {                                                                                  │
 │    142  +                                         label += ': ';                                                                            │
 │    143  +                                     }                                                                                             │
 │    144  +                                     if (context.parsed.y !== null) {                                                              │
 │    145  +                                         label += new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'PLN'              │
 │           }).format(context.parsed.y);                                                                                                      │
 │    146  +                                     }                                                                                             │
 │    147  +                                     return label;                                                                                 │
 │    148  +                                 }                                                                                                 │
 │    149  +                             }                                                                                                     │
 │    150  +                         }                                                                                                         │
 │    151  +                     }                                                                                                             │
 │    152  +                 }                                                                                                                 │
 │    153  +             });                                                                                                                   │
 │    154  +         }                                                                                                                         │
 │    155  +     });                                                                                                                           │
 │    156  +     {% endif %}                                                                                                                   │
 │    157  + });                                                                                                                               │
 │    158  + </script>                                                                                                                         │
 │    159  + {% endblock %}                                                                                                                    │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Zakończyłem implementację Widżetu 2: Wykres Liniowy.

  Teraz, po wybraniu rodzaju roboty, pod statystykami powinien pojawić się wykres liniowy pokazujący, jak średnia cena dla tej roboty zmieniała się w
  czasie.

  Przechodzę do Widżetu 3: Wykres Słupkowy - Porównanie Cen wg Wykonawcy.

  Proces będzie analogiczny: najpierw stworzę endpoint API w routes.py, a następnie dodam kod JavaScript i element <canvas> w szablonie.

  Zaczynam od routes.py.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit app/tenders/routes.py:     labels = [row[0] for row i... =>     labels = [row[0] for row i...                                       │
 │                                                                                                                                             │
 │    649        values = [float(row[1]) for row in data]                                                                                      │
 │    650                                                                                                                                      │
 │    651        return jsonify({'labels': labels, 'values': values})                                                                          │
 │    652  +                                                                                                                                   │
 │    653  + @tenders_bp.route('/api/price_by_contractor/<int:work_type_id>')                                                                  │
 │    654  + @login_required                                                                                                                   │
 │    655  + def price_by_contractor_data(work_type_id):                                                                                       │
 │    656  +     """                                                                                                                           │
 │    657  +     Zwraca dane do wykresu porównania cen wg wykonawcy dla danego rodzaju roboty.                                                 │
 │    658  +     """                                                                                                                           │
 │    659  +     data = db.session.query(                                                                                                      │
 │    660  +         Firmy.nazwa_firmy,                                                                                                        │
 │    661  +         func.avg(UnitPrice.cena_jednostkowa)                                                                                      │
 │    662  +     ).join(Tender, UnitPrice.id_oferty == Tender.id)\n     .join(Firmy, Tender.id_firmy == Firmy.id_firmy)\                       │
 │    663  +      .filter(UnitPrice.id_work_type == work_type_id)\                                                                             │
 │    664  +      .group_by(Firmy.nazwa_firmy)\                                                                                                │
 │    665  +      .order_by(func.avg(UnitPrice.cena_jednostkowa).desc())\                                                                      │
 │    666  +      .all()                                                                                                                       │
 │    667  +                                                                                                                                   │
 │    668  +     labels = [row[0] for row in data]                                                                                             │
 │    669  +     values = [float(row[1]) for row in data]                                                                                      │
 │    670  +                                                                                                                                   │
 │    671  +     return jsonify({'labels': labels, 'values': values})                                                                          │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Endpoint API jest gotowy.

  Teraz dodam odpowiedni kod do szablonu analysis_dashboard.html, aby wygenerować wykres słupkowy. Umieszczę go obok wykresu liniowego, aby oba były
  widoczne jednocześnie.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit ...app/templates/analysis_dashboard.html:         <div class="row mt-4">... =>         <div class="row mt-4">...                    │
 │                                                                                                                                             │
 │    73         </div>                                                                                                                        │
 │    74     </div>                                                                                                                            │
 │    75     <div class="row mt-4">                                                                                                            │
 │    76   -     <div class="col-md-12">                                                                                                       │
 │    77   -         <div class="card">                                                                                                        │
 │    76   +     <div class="col-lg-6">                                                                                                        │
 │    77   +         <div class="card h-100">                                                                                                  │
 │    78                 <div class="card-header">                                                                                             │
 │    79                     <h4 class="card-title">Ewolucja Ceny w Czasie</h4>                                                                │
 │    80                 </div>                                                                                                                │
 │    83                 </div>                                                                                                                │
 │    84             </div>                                                                                                                    │
 │    85         </div>                                                                                                                        │
 │    86   +     <div class="col-lg-6">                                                                                                        │
 │    87   +         <div class="card h-100">                                                                                                  │
 │    88   +             <div class="card-header">                                                                                             │
 │    89   +                 <h4 class="card-title">Średnia Cena wg Wykonawcy</h4>                                                             │
 │    90                 </div>                                                                                                                │
 │    91   +             <div class="card-body">                                                                                               │
 │    92   +                 <canvas id="priceByContractorChart"></canvas>                                                                     │
 │    93   +             </div>                                                                                                                │
 │    94   +         </div>                                                                                                                    │
 │    95   +     </div>                                                                                                                        │
 │    96   + </div>                                                                                                                            │
 │    97     {% else %}                                                                                                                        │
 │    98     <div class="alert alert-info mt-4">Brak danych cenowych dla wybranego rodzaju roboty.</div>                                       │
 │    99     {% endif %}                                                                                                                       │
 ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
✦ Teraz dodam kod JavaScript do generowania drugiego wykresu.
 ╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ ✔  Edit ...app/templates/analysis_dashboard.html:     // Wykres Ewolucji Ceny... =>     // Wykres Ewolucji Ceny...                          │
 │                                                                                                                                             │
 │    163                });                                                                                                                   │
 │    164            }                                                                                                                         │
 │    165        });                                                                                                                           │
 │    166  +                                                                                                                                   │
 │    167  +     // Wykres Cen wg Wykonawcy                                                                                                    │
 │    168  +     $.ajax({                                                                                                                      │
 │    169  +         url: `/tenders/api/price_by_contractor/{{ selected_work_type_id }}`,                                                      │
 │    170  +         success: function(data) {                                                                                                 │
 │    171  +             const ctx = document.getElementById('priceByContractorChart').getContext('2d');                                       │
 │    172  +             new Chart(ctx, {                                                                                                      │
 │    173  +                 type: 'bar',                                                                                                      │
 │    174  +                 data: {                                                                                                           │
 │    175  +                     labels: data.labels,                                                                                          │
 │    176  +                     datasets: [{                                                                                                  │
 │    177  +                         label: 'Średnia cena',                                                                                    │
 │    178  +                         data: data.values,                                                                                        │
 │    179  +                         backgroundColor: 'rgba(153, 102, 255, 0.6)',                                                              │
 │    180  +                         borderColor: 'rgba(153, 102, 255, 1)',                                                                    │
 │    181  +                         borderWidth: 1                                                                                            │
 │    182  +                     }]                                                                                                            │
 │    183  +                 },                                                                                                                │
 │    184  +                 options: {                                                                                                        │
 │    185  +                     indexAxis: 'y', // Osie zamienione miejscami dla lepszej czytelności                                          │
 │    186  +                     scales: {                                                                                                     │
 │    187  +                         x: {                                                                                                      │
 │    188  +                             beginAtZero: true,                                                                                    │
 │    189  +                             ticks: {                                                                                              │
 │    190  +                                 callback: function(value, index, values) {                                                        │
 │    191  +                                     return value.toFixed(2) + ' zł';                                                              │
 │    192  +                                 }                                                                                                 │
 │    193  +                             }                                                                                                     │
 │    194  +                         }                                                                                                         │
 │    195  +                     },                                                                                                            │
 │    196  +                     plugins: {                                                                                                    │
 │    197  +                         legend: {                                                                                                 │
 │    198  +                             display: false                                                                                        │
 │    199  +                         },                                                                                                        │
 │    200  +                         tooltip: {                                                                                                │
 │    201  +                             callbacks: {                                                                                          │
 │    202  +                                 label: function(context) {                                                                        │
 │    203  +                                     let label = context.dataset.label || '';                                                      │
 │    204  +                                     if (label) {                                                                                  │
 │    205  +                                         label += ': ';                                                                            │
 │    206  +                                     }                                                                                             │
 │    207  +                                     if (context.parsed.x !== null) {                                                              │
 │    208  +                                         label += new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'PLN'              │
 │           }).format(context.parsed.x);                                                                                                      │
 │    209  +                                     }                                                                                             │
 │    210  +                                     return label;                                                                                 │
 │    211  +                                 }                                                                                                 │
 │    212  +                             }                                                                                                     │
 │    213  +                         }                                                                                                         │
 │    214  +                     }                                                                                                             │
 │    215  +                 }                                                                                                                 │
 │    216  +             });                                                                                                                   │
 │    217  +         }                                                                                                                         │
 │    218  +     });                                                                                                                           │
 │    219        {% endif %}                                                                                                                   │
 │    220    });                                                                                                                               │
 │    221    </script>                                                                                                                         │