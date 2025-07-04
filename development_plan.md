### Szczegółowy Plan Rozbudowy Aplikacji

#### **Faza 0: Przygotowanie Środowiska i Narzędzi**

Zanim napiszemy jakikolwiek kod aplikacji, musimy przygotować narzędzia.

*   **Krok 1: Instalacja Zależności**
    *   **Akcja:** Dodam do projektu i zainstaluję biblioteki niezbędne do obsługi plików i migracji: `alembic` (do migracji bazy danych), `PyMuPDF` (do ekstrakcji tekstu z PDF), `pytesseract` i `Pillow` (do OCR z obrazów), `openpyxl` (do plików Excel) oraz `python-magic` (do identyfikacji typów plików).
    *   **Cel:** Zapewnienie, że mamy wszystkie narzędzia potrzebne do dalszej pracy.
    *   **Weryfikacja:** Pomyślne wykonanie `pip install -r requirements.txt` po dodaniu nowych bibliotek. Aplikacja musi się nadal uruchamiać bez błędów importu.

*   **Krok 2: Konfiguracja Migracji (Alembic)**
    *   **Akcja:** Zainicjuję i skonfiguruję Alembic w projekcie. Skonfiguruję go tak, aby łączył się z Twoją bazą danych na Neon.tech, używając `DATABASE_URL` z pliku `.env`.
    *   **Cel:** Stworzenie mechanizmu do bezpiecznego i wersjonowanego zarządzania zmianami w schemacie bazy danych.
    *   **Weryfikacja:** Wykonanie komendy `alembic current` powinno pomyślnie połączyć się z bazą i nie zwrócić żadnych błędów (nawet jeśli nie ma jeszcze żadnych migracji).

*   **Krok 3: Konfiguracja Przechowywania Plików**
    *   **Akcja:** W pliku `config.py` dodam zmienną `UPLOAD_FOLDER`, która będzie wskazywać na lokalny katalog (np. `instance/uploads`), gdzie tymczasowo będziemy przechowywać wgrane pliki.
    *   **Cel:** Przygotowanie miejsca do zapisywania plików ofert.
    *   **Weryfikacja:** Aplikacja uruchamia się poprawnie, a po uruchomieniu w katalogu `instance` tworzony jest podkatalog `uploads`.

---

#### **Faza 1: Moduł Ofert (Tenders) - Backend i Struktura Danych**

*   **Krok 4: Stworzenie Modeli Bazy Danych**
    *   **Akcja:** W pliku `app/models.py` zdefiniuję nowy model `Tender` z polami: `id`, `nazwa_oferty`, `data_otrzymania`, `status`, `id_firmy` (klucz obcy), `original_filename`, `storage_path`, `file_type`.
    *   **Cel:** Zdefiniowanie struktury tabeli do przechowywania informacji o ofertach.
    *   **Weryfikacja:** Wykonanie `alembic revision --autogenerate` musi poprawnie wygenerować nowy plik migracji. Następnie `alembic upgrade head` musi bezbłędnie zaaplikować zmiany na bazie Neon.tech. Istnienie nowej tabeli `tender` w bazie potwierdzi sukces.

*   **Krok 5: Stworzenie Formularza Oferty**
    *   **Akcja:** W `app/forms.py` stworzę klasę `TenderForm` zawierającą pola do wprowadzania danych oferty oraz pole `FileField` do wgrywania pliku.
    *   **Cel:** Przygotowanie formularza do interakcji z użytkownikiem.
    *   **Weryfikacja:** Aplikacja musi się nadal uruchamiać bez błędów składniowych.

*   **Krok 6: Stworzenie Blueprintu i Podstawowych Tras**
    *   **Akcja:** Stworzę nową strukturę katalogów `app/tenders/` z plikami `__init__.py` i `routes.py`. Zdefiniuję w nim `tenders_bp` i zarejestruję go w `app/__init__.py`. Stworzę szkielety tras: `GET /tenders` (lista) oraz `GET, POST /tenders/new` (dodawanie).
    *   **Cel:** Zbudowanie szkieletu nowego modułu i podłączenie go do aplikacji.
    *   **Weryfikacja:** Po uruchomieniu aplikacji, wejście na adres `/tenders` nie powinno powodować błędu serwera (może zwrócić 404, jeśli szablon nie istnieje, co jest w tym momencie OK).

*   **Krok 7: Implementacja Logiki Dodawania Oferty**
    *   **Akcja:** W `app/tenders/routes.py` zaimplementuję logikę dla metody `POST` na trasie `/tenders/new`. Logika ta będzie: walidować formularz, zapisywać wgrany plik w `UPLOAD_FOLDER`, tworzyć nowy obiekt `Tender` w bazie danych z odpowiednimi danymi.
    *   **Cel:** Umożliwienie realnego dodawania ofert z plikami do systemu.
    *   **Weryfikacja:** Stworzymy tymczasowy, prosty szablon `tender_form.html`. Po przejściu na `/tenders/new`, wypełnieniu formularza i wysłaniu go, musimy zaobserwować trzy rzeczy: 1) Plik pojawił się w katalogu `instance/uploads`. 2) W tabeli `tender` w bazie danych pojawił się nowy wiersz. 3) Użytkownik został przekierowany na inną stronę (np. listę ofert).

---

#### **Faza 2: Moduł Ofert (Tenders) - Interfejs Użytkownika**

*   **Krok 8: Widok Listy Ofert i Nawigacja**
    *   **Akcja:** Uzupełnię logikę trasy `GET /tenders`, aby pobierała wszystkie oferty z bazy. Stworzę szablon `tenders_list.html` wyświetlający oferty w tabeli. Dodam link "Oferty" w głównym menu nawigacyjnym w `base.html`.
    *   **Cel:** Umożliwienie użytkownikowi przeglądania wszystkich dodanych ofert.
    *   **Weryfikacja:** Po wejściu na `/tenders`, oferta dodana w kroku 7 musi być widoczna na liście. Link w menu nawigacyjnym musi działać.

*   **Krok 9: Widok Szczegółów Oferty**
    *   **Akcja:** Stworzę trasę `GET /tenders/<int:tender_id>` oraz szablon `tender_details.html`. Będą one wyświetlać wszystkie dane konkretnej oferty oraz link do pobrania oryginalnego pliku.
    *   **Cel:** Umożliwienie wglądu w szczegóły pojedynczej oferty.
    *   **Weryfikacja:** Kliknięcie na ofertę na liście musi przenieść do strony szczegółów. Wyświetlone dane muszą być poprawne, a link do pobrania pliku musi działać.

*  ** Krok 10: Implementacja Modułu Projektów (CRUD)**
       * Akcja 1.1 (Model): W app/models.py stworzę nowy model Project (id, nazwa_projektu). Zaktualizuję model Tender, dodając do niego klucz
         obcy id_projektu.
       * Akcja 1.2 (Migracja): Wygeneruję i zastosuję nową migrację Alembic, aby fizycznie stworzyć tabelę projects w bazie danych i dodać nową
         kolumnę do tabeli tenders.
       * Akcja 1.3 (Formularz): W app/forms.py stworzę prosty ProjectForm do dodawania i edycji projektów.
       * Akcja 1.4 (Trasy i Widoki): W app/main_routes.py dodam pełen zestaw tras CRUD (/projects, /projects/new, /projects/<id>/edit,
         /projects/<id>/delete) do zarządzania projektami. Stworzę też odpowiednie szablony (projects.html i wykorzystam simple_form.html).
       * Cel: Stworzenie w pełni funkcjonalnego, samodzielnego modułu do zarządzania projektami.
       * Weryfikacja: Będzie można dodawać, edytować i usuwać projekty z poziomu interfejsu użytkownika.


   * Krok 11: Integracja Projektów z Ofertami
       * Akcja: Zmodyfikuję formularz TenderForm w app/forms.py, dodając pole SelectField (id_projektu), które pozwoli wybrać projekt podczas
         tworzenia/edycji oferty. Zaktualizuję również logikę w app/tenders/routes.py, aby zapisywała to powiązanie.
       * Cel: Umożliwienie przypisywania ofert do konkretnych projektów.
       * Weryfikacja: Podczas dodawania lub edycji oferty w formularzu pojawi się lista rozwijana z projektami. Wybrany projekt zostanie
         poprawnie zapisany w bazie danych.

Faza 2: Moduł Ofert - Pełna Integracja z Interfejsem Użytkownika


   * Krok 12: Integracja z Widokiem Szczegółów Firmy
       * Akcja: Zmodyfikuję szablon app/templates/company_details.html. Dodam nową zakładkę lub sekcję o nazwie "Oferty", w której będzie
         wyświetlana tabela z listą wszystkich ofert złożonych przez daną firmę. Każdy wiersz będzie linkiem do strony szczegółów tej oferty.
       * Cel: Zapewnienie szybkiego dostępu do ofert powiązanych z konkretną firmą.
       * Weryfikacja: Po wejściu na stronę szczegółów firmy, która ma przypisane oferty, zobaczymy ich listę.


   * Krok 13: Implementacja Filtrowania i Wyszukiwania na Liście Ofert
       * Akcja 13.1 (Interfejs): W szablonie app/tenders/templates/tenders_list.html dodam formularz z metodą GET, zawierający pola <select> do
         filtrowania po firmie i po projekcie.
       * Akcja 13.2 (Logika): Zmodyfikuję trasę list_tenders w app/tenders/routes.py. Będzie ona odczytywać parametry z adresu URL
         (?id_firmy=...&id_projektu=...) i na ich podstawie dynamicznie budować zapytanie do bazy danych, aby zwracać tylko przefiltrowane
         wyniki.
       * Cel: Umożliwienie użytkownikom łatwego odnajdywania interesujących ich ofert.
       * Weryfikacja: Wybranie firmy lub projektu z listy rozwijanej i kliknięcie "Filtruj" spowoduje przeładowanie strony i wyświetlenie tylko
         tych ofert, które spełniają wybrane kryteria.


Implementacji modułu Cen Jednostkowych
Ekstrakcją danych z plików PDF/obrazów?