# Finalny, Kompletny i Recepturowy Plan Importu Danych

**Wersja:** Ostateczna (z pełną definicją tabel)
**Cel:** Stworzyć precyzyjną "książkę kucharską", gdzie każda tabela ma swoją recepturę, eliminując wszelkie wątpliwości.

---
## **Wprowadzenie**
Ta instrukcja jest ostateczna. Każda tabela, którą musimy stworzyć, ma poniżej swój dedykowany rozdział z dokładną listą kolumn do utworzenia. Proszę postępować ściśle według tych "receptur".

**Przypomnienie o prefiksie `syb_`:**
Kiedy tworzysz nową kolumnę (np. `Legacy Category ID`), system zapisuje ją z prefiksem (np. `syb_legacycategoryid`). W Dataflow zawsze szukaj nazwy z tym prefiksem!

---
### **Krok 1 i 2: Firmy (`Account`) i Osoby (`Contact`)**
**Status: UKOŃCZONE.**

---
### **Krok 3: Import Tabel Słownikowych (Dane Podstawowe)**

#### **3.1. Receptura: Tabela `Category`**
*   **A. Tworzenie Tabeli `Category`:**
    *   W rozwiązaniu stwórz tabelę `Category` (`Plural name`: `Categories`).
    *   Główna kolumna (`Primary column`) powinna nazywać się `Name`.
    *   Dodaj **jedną** nową kolumnę:
        *   `Display name`: `Legacy Category ID`, `Data type`: `Single line of text`.
*   **B. Klucz Alternatywny (AK):** Stwórz AK na kolumnie `Legacy Category ID`.
*   **C. Dataflow (`Dataflow_Category`):**
    *   Źródło: `categories.csv`.
    *   Cel: Tabela `Category`.
    *   Mapowanie: `id` -> `Legacy Category ID`, `nazwa_kategorii` -> `Name`.

#### **3.2. Receptura: Tabela `Specialty`**
*   **A. Tworzenie Tabeli `Specialty`:**
    *   Stwórz tabelę `Specialty` (`Plural name`: `Specialties`), główna kolumna `Name`.
    *   Dodaj kolumnę: `Legacy Specialty ID` (`Single line of text`).
*   **B. AK:** Stwórz AK na `Legacy Specialty ID`.
*   **C. Dataflow (`Dataflow_Specialty`):**
    *   Źródło: `specjalnosci.csv`.
    *   Mapowanie: `id_specjalnosci` -> `Legacy Specialty ID`, `specjalnosc` -> `Name`.

#### **3.3. Receptura: Tabela `Project`**
*   **A. Tworzenie Tabeli `Project`:**
    *   Stwórz tabelę `Project` (`Plural name`: `Projects`), główna kolumna `Name`.
    *   Dodaj kolumny:
        *   `Legacy Project ID` (`Single line of text`)
        *   `Abbreviation` (`Single line of text`)
        *   `Type` (`Single line of text`)
        *   `Notes` (`Multiple lines of text`)
*   **B. AK:** Stwórz AK na `Legacy Project ID`.
*   **C. Dataflow (`Dataflow_Project`):**
    *   Źródło: `projects.csv`.
    *   Mapowanie: `id` -> `Legacy Project ID`, `nazwa_projektu` -> `Name`, `skrot` -> `Abbreviation`, `rodzaj` -> `Type`, `uwagi` -> `Notes`.

#### **3.4. Receptura: Tabela `Voivodeship`**
*   **A. Tworzenie Tabeli `Voivodeship`:**
    *   Stwórz tabelę `Voivodeship` (`Plural name`: `Voivodeships`), główna kolumna `Name`.
    *   Dodaj kolumnę: `Legacy Voivodeship ID` (`Single line of text`).
*   **B. AK:** Stwórz AK na `Legacy Voivodeship ID`.
*   **C. Dataflow (`Dataflow_Voivodeship`):**
    *   Źródło: `wojewodztwa.csv`.
    *   Mapowanie: `id_wojewodztwa` -> `Legacy Voivodeship ID`, `wojewodztwo` -> `Name`.

#### **3.5. Receptura: Tabela `County`**
*   **A. Tworzenie Tabeli `County`:**
    *   Stwórz tabelę `County` (`Plural name`: `Counties`), główna kolumna `Name`.
    *   Dodaj kolumny:
        *   `Legacy County ID` (`Single line of text`)
        *   `Voivodeship` (`Data type`: **`Lookup`**, `Related table`: **`Voivodeship`**)
*   **B. AK:** Stwórz AK na `Legacy County ID`.
*   **C. Dataflow (`Dataflow_County`):**
    *   Źródło: `powiaty.csv`.
    *   Mapowanie: `id_powiaty` -> `Legacy County ID`, `powiat` -> `Name`, `id_wojewodztwa` -> `Voivodeship` (Lookup).

#### **3.6. Receptura: Tabela `Work Type`**
*   **A. Tworzenie Tabeli `Work Type`:**
    *   Stwórz tabelę `Work Type` (`Plural name`: `Work Types`), główna kolumna `Name`.
    *   Dodaj kolumny:
        *   `Legacy Work Type ID` (`Single line of text`)
        *   `Category` (`Data type`: **`Lookup`**, `Related table`: **`Category`**)
*   **B. AK:** Stwórz AK na `Legacy Work Type ID`.
*   **C. Dataflow (`Dataflow_WorkType`):**
    *   Źródło: `work_types.csv`.
    *   Mapowanie: `id` -> `Legacy Work Type ID`, `name` -> `Name`, `id_kategorii` -> `Category` (Lookup).

---
### **Krok 4: Receptury: Dane Powiązane z Firmą**

#### **4.1. Receptura: Tabela `Address`**
*   **A. Tworzenie Tabeli `Address`:**
    *   Stwórz tabelę `Address` (`Plural name`: `Addresses`), główna kolumna `Name`.
    *   Dodaj kolumny:
        *   `Legacy Address ID` (`Single line of text`)
        *   `Account` (`Data type`: **`Lookup`**, `Related table`: **`Account`**)
        *   `Street` (`Single line of text`)
        *   `City` (`Single line of text`)
        *   `Postal Code` (`Single line of text`)
        *   `Address Type` (`Data type`: **`Choice`**). Ręcznie dodaj opcje z pliku `adresy_typ.csv`.
*   **B. AK:** Stwórz AK na `Legacy Address ID`.
*   **C. Dataflow (`Dataflow_Address`):** Scal `adresy.csv` z `adresy_typ.csv`. Mapuj `id_adresy` -> `Legacy Address ID`, `id_firmy` -> `Account` (Lookup), `ulica_miejscowosc` -> `Street`, `miejscowosc` -> `City`, `kod` -> `Postal Code`, `typ_adresu` (ze scalenia) -> `Address Type`.

#### **4.2. Receptura: Tabela `Email`**
*   **A. Tworzenie Tabeli `Email`:**
    *   Stwórz tabelę `Email` (`Plural name`: `Emails`), główna kolumna `Name`.
    *   Dodaj kolumny:
        *   `Legacy Email ID` (`Single line of text`)
        *   `Account` (`Data type`: **`Lookup`**, `Related table`: **`Account`**)
        *   `Email Address` (`Data type`: `Email`)
        *   `Email Type` (`Data type`: **`Choice`**). Ręcznie dodaj opcje z pliku `email_typ.csv`.
*   **B. AK:** Stwórz AK na `Legacy Email ID`.
*   **C. Dataflow (`Dataflow_Email`):** Scal `email.csv` z `email_typ.csv`. Mapuj `id_email` -> `Legacy Email ID`, `id_firmy` -> `Account` (Lookup), `e_mail` -> `Email Address`, `typ_emaila` (ze scalenia) -> `Email Type`.

#### **4.3. Receptura: Tabela `Phone`**
*   **A. Tworzenie Tabeli `Phone`:**
    *   Stwórz tabelę `Phone` (`Plural name`: `Phones`), główna kolumna `Name`.
    *   Dodaj kolumny:
        *   `Legacy Phone ID` (`Single line of text`)
        *   `Account` (`Data type`: **`Lookup`**, `Related table`: **`Account`**)
        *   `Phone Number` (`Data type`: `Phone`)
        *   `Phone Type` (`Data type`: **`Choice`**). Ręcznie dodaj opcje z pliku `telefon_typ.csv`.
*   **B. AK:** Stwórz AK na `Legacy Phone ID`.
*   **C. Dataflow (`Dataflow_Phone`):** Scal `telefon.csv` z `telefon_typ.csv`. Mapuj `id_telefon` -> `Legacy Phone ID`, `id_firmy` -> `Account` (Lookup), `telefon` -> `Phone Number`, `typ_telefonu` (ze scalenia) -> `Phone Type`.

---
### **Krok 5: Receptury: Pozostałe Dane**

#### **5.1. Receptura: Tabela `Rating`**
*   **A. Tworzenie Tabeli `Rating`:**
    *   Stwórz tabelę `Rating` (`Plural name`: `Ratings`), główna kolumna `Name`.
    *   Dodaj kolumny:
        *   `Legacy Rating ID` (`Single line of text`)
        *   `Account` (`Data type`: **`Lookup`**, `Related table`: **`Account`**)
        *   `Reviewer` (`Single line of text`)
        *   `Project Department` (`Single line of text`)
        *   `Year of Cooperation` (`Data type`: `Whole Number`)
        *   `Rating Value` (`Data type`: `Whole Number`)
        *   `Comment` (`Multiple lines of text`)
*   **B. AK:** Stwórz AK na `Legacy Rating ID`.
*   **C. Dataflow (`Dataflow_Rating`):** Mapuj `oceny_id` -> `Legacy Rating ID`, `id_firmy` -> `Account`, `osoba_oceniajaca` -> `Reviewer`, `budowa_dzial` -> `Project Department`, `rok_wspolpracy` -> `Year of Cooperation`, `ocena` -> `Rating Value`, `komentarz` -> `Comment`.

#### **5.2. Receptura: Tabela `Tender`**
*   **A. Tworzenie Tabeli `Tender`:**
    *   Stwórz tabelę `Tender` (`Plural name`: `Tenders`), główna kolumna `Name`.
    *   Dodaj kolumny:
        *   `Legacy Tender ID` (`Single line of text`)
        *   `Account` (`Data type`: **`Lookup`**, `Related table`: **`Account`**)
        *   `Project` (`Data type`: **`Lookup`**, `Related table`: **`Project`**)
        *   `Received Date` (`Data type`: `Date and Time`)
        *   `Status` (`Data type`: **`Choice`**). Ręcznie dodaj opcje: "Nowa", "Złożono", "Anulowano", etc.
        *   `Extracted Content` (`Multiple lines of text`)
*   **B. AK:** Stwórz AK na `Legacy Tender ID`.
*   **C. Dataflow (`Dataflow_Tender`):** Mapuj `id` -> `Legacy Tender ID`, `nazwa_oferty` -> `Name`, `id_firmy` -> `Account`, `id_projektu` -> `Project`, `data_otrzymania` -> `Received Date`, `status` -> `Status`, `extracted_content` -> `Extracted Content`.

#### **5.3. Receptura: Tabela `Unit Price`**
*   **A. Tworzenie Tabeli `Unit Price`:**
    *   Stwórz tabelę `Unit Price` (`Plural name`: `Unit Prices`), główna kolumna `Name`.
    *   Dodaj kolumny:
        *   `Legacy Unit Price ID` (`Single line of text`)
        *   `Tender` (`Data type`: **`Lookup`**, `Related table`: **`Tender`**)
        *   `Work Type` (`Data type`: **`Lookup`**, `Related table`: **`Work Type`**)
        *   `Category` (`Data type`: **`Lookup`**, `Related table`: **`Category`**)
        *   `Unit of Measure` (`Single line of text`)
        *   `Price` (`Data type`: `Decimal Number`)
        *   `Notes` (`Multiple lines of text`)
*   **B. AK:** Stwórz AK na `Legacy Unit Price ID`.
*   **C. Dataflow (`Dataflow_UnitPrice`):** Mapuj `id` -> `Legacy Unit Price ID`, `id_oferty` -> `Tender`, `id_work_type` -> `Work Type`, `id_kategorii` -> `Category`, `jednostka_miary` -> `Unit of Measure`, `cena_jednostkowa` -> `Price`, `uwagi` -> `Notes`.

---
### **Krok 6: Relacje Wiele-do-Wielu**
*Metoda pozostaje bez zmian (Power Automate dla `firmyspecjalnosci.csv` i Dataflow dla `firmyobszardzialania.csv` po stworzeniu tabeli `Operating Area` z odpowiednimi kolumnami Lookup).*
✦ Doskonale, przechodzimy do ostatniego etapu importu danych – tworzenia relacji wiele-do-wielu (N:N). To kluczowy krok, który połączy firmy z ich
  specjalizacjami i obszarami działania.

  Zgodnie z planem, użyjemy dwóch różnych metod, abyś poznał obie techniki. Poniżej znajduje się szczegółowa instrukcja krok po kroku dla każdej z nich.

  ---

  Metoda 1: Power Automate dla relacji Firma-Specjalizacja (`firmyspecjalnosci.csv`)

  Użyjemy tej metody do połączenia istniejących już rekordów Firm (Account) z istniejącymi rekordami Specjalizacji (Specialty). Power Automate świetnie nadaje
   się do takich operacji.

  Krok 1: Przygotowanie pliku

   1. Otwórz plik firmyspecjalnosci.csv w programie Excel.
   2. Sformatuj dane jako tabelę (Ctrl+T). To ważne, aby Power Automate mógł je łatwo odczytać.
   3. Zapisz ten plik Excel w lokalizacji dostępnej dla Power Automate, np. w OneDrive for Business lub w bibliotece dokumentów SharePoint.

  Krok 2: Budowa przepływu (Flow) w Power Automate

   1. Przejdź do Power Apps, a następnie do sekcji Przepływy (Flows).
   2. Stwórz nowy przepływ: Błyskawiczny przepływ w chmurze (Instant cloud flow).
   3. Nazwij go np. Import Relacji Firma-Specjalizacja, wybierz wyzwalacz Ręcznie wyzwól przepływ (Manually trigger a flow) i kliknij Utwórz.

  Krok 3: Konfiguracja akcji w przepływie

  Teraz dodamy kolejne kroki do naszego przepływu:

   1. + Nowy krok: Dodaj akcję "Wyświetl listę wierszy obecnych w tabeli" (List rows present in a table) z konektora Excel Online (Business).
       * Lokalizacja: Wskaż OneDrive lub SharePoint.
       * Biblioteka dokumentów: Wybierz odpowiednią bibliotekę.
       * Plik: Wskaż zapisany plik Excel.
       * Tabela: Wybierz tabelę, którą stworzyłeś w pliku (zwykle Tabela1).

   2. + Nowy krok: Dodaj akcję "Zastosuj do każdego" (Apply to each).
       * W polu "Wybierz dane wyjściowe z poprzednich kroków" wybierz `value` z akcji Excela. Wewnątrz tej pętli będziemy przetwarzać każdy wiersz z pliku.

   3. Wewnątrz pętli "Apply to each" dodaj akcje:

      a. Znajdź Firmę: Dodaj akcję "Wyświetl listę wierszy" (List rows) z konektora Microsoft Dataverse.
       * Nazwa tabeli: Wybierz Accounts.
       * Filtruj wiersze (Filter Rows): To najważniejsza część. Wpisz zapytanie OData, aby znaleźć firmę po jej starym ID. Składnia: `syb_legacyaccountid eq '@{items('Apply_to_each')?['id_firmy']}'`
           * `syb_legacyaccountid` to nazwa schematu Twojej kolumny z Legacy ID w tabeli Account.
           * `@{...}` to dynamiczna zawartość z kolumny `id_firmy` z pliku Excel.

      b. Znajdź Specjalizację: Dodaj kolejną akcję "Wyświetl listę wierszy" (List rows) z konektora Microsoft Dataverse.
       * Nazwa tabeli: Wybierz Specialties.
       * Filtruj wiersze (Filter Rows): Wpisz podobne zapytanie: `syb_legacyspecialtyid eq '@{items('Apply_to_each')?['id_specjalnosci']}'`

      c. Stwórz Relację: Dodaj akcję "Powiąż wiersze" (Relate rows) z konektora Microsoft Dataverse.
       * Nazwa tabeli: Wybierz Accounts.
       * Identyfikator wiersza (Row ID): Wstaw ID znalezionej firmy. Użyj wyrażenia: `first(outputs('Znajdź_Firmę')?['body/value'])?['accountid']`
       * Nazwa relacji (Relationship): Wpisz nazwę schematu relacji N:N między firmami a specjalizacjami (np. `syb_account_syb_specialty_syb_specialty`).
       * Powiąż z adresem URL zasobu (Relate with Resource URL): Wstaw pełny URL do znalezionej specjalizacji. Użyj wyrażenia:
         `@{first(outputs('Znajdź_Specjalizację')?['body/value'])?['@odata.id']}`

   4. Zapisz i Testuj: Zapisz przepływ. Uruchom go testowo dla kilku pierwszych wierszy, a gdy upewnisz się, że działa poprawnie, uruchom dla całego pliku.

  ---

  Metoda 2: Dataflow dla relacji Firma-Obszar Działania (`firmyobszardzialania.csv`)

  Ta metoda wymaga stworzenia nowej, pośredniczącej tabeli (tzw. tabeli skrzyżowaniowej lub "Intersect Table").

  Krok 1: Stworzenie tabeli pośredniczącej `Operating Area`

   1. W swoim rozwiązaniu w Power Apps stwórz nową tabelę.
   2. Nazwa wyświetlana: Operating Area, Nazwa w liczbie mnogiej: Operating Areas.
   3. Główna kolumna: Zostaw Name, ale w kolejnym kroku ustawimy ją jako opcjonalną.
   4. Dodaj dwie kluczowe kolumny:
       * Kolumna 1:
           * Display name: Account
           * Data type: `Lookup`
           * Related table: `Account`
           * Ustaw jako wymaganą (Required).
       * Kolumna 2:
           * Display name: County
           * Data type: `Lookup`
           * Related table: `County`
           * Ustaw jako wymaganą (Required).
   5. Dostosuj główną kolumnę `Name`: Wejdź w jej edycję i zmień jej wymaganie z Wymagane biznesowo (Business Required) na Opcjonalne (Optional).
   6. Zapisz i opublikuj tabelę.

  Krok 2: Stworzenie i konfiguracja Dataflow

   1. Przejdź do sekcji Przepływy danych (Dataflows) i stwórz nowy, np. Dataflow_OperatingArea.
   2. Źródło danych: Wybierz plik firmyobszardzialania.csv.
   3. Edytor Power Query:
       * Upewnij się, że typy danych dla kolumn id_firmy i id_powiatu są ustawione jako Tekst (Text).
       * (Opcjonalnie, ale zalecane) Dodaj kolumnę niestandardową (Add Column -> Custom Column), aby stworzyć czytelną nazwę dla głównej kolumny Name. Nazwij ją
          np. Name i użyj formuły [id_firmy] & " - " & [id_powiatu].
   4. Mapowanie danych:
       * Cel: Wybierz nowo stworzoną tabelę Operating Area.
       * Mapowanie kolumn:
           * id_firmy -> Account (Lookup: syb_legacyaccountid)
           * id_powiatu -> County (Lookup: syb_legacycountyid)
           * Twoja kolumna niestandardowa -> Name
       * Klucz alternatywny: Nie musisz go ustawiać, ponieważ relacje lookup zapewnią unikalność.
   5. Zapisz i uruchom Dataflow.
  Po wykonaniu obu tych kroków, wszystkie Twoje dane zostaną w pełni zaimportowane i połączone