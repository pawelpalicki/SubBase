# Plan Importu Danych do Dataverse - Wersja 5 (Kompletna i Szczegółowa)

Ten plan opisuje krok po kroku proces importu wszystkich tabel do Dataverse. Jest to wersja bardzo szczegółowa, przeznaczona dla początkującego użytkownika, aby uniknąć wszelkich niejasności. Plan uwzględnia najlepsze praktyki Dataverse, takie jak użycie pól **Choice** dla statusów i typów.

**Nasza strategia:** Dla każdej importowanej tabeli wykonujemy te same, powtarzalne kroki, tworząc dla niej osobny Dataflow.

---

## **Grupa 1, 2, 3: Tabele Podstawowe (Ukończone)**

*Zakładamy, że tabele `Category`, `Specialty`, `Project`, `Account`, `Contact`, `Voivodeship`, `County` i `Work Type` zostały już poprawnie zaimportowane zgodnie z poprzednimi krokami.*

---

## **Grupa 4: Tabele z wieloma zależnościami**

### **4.1. Tabela: `Operating Area` (z `firmyobszardzialania.csv`)**

*   **A. Ręczne tworzenie tabeli `Operating Area`:**
    1.  W rozwiązaniu `SubBase Core`, kliknij **`+ New`** -> **`Table`** -> **`Table`**.
    2.  `Display name`: `Operating Area`, `Plural name`: `Operating Areas`.
    3.  W zakładce **`Columns`**, dodaj kolumny:
        *   `Account` (typ: **Lookup**, `Related table`: `Account`)
        *   `Voivodeship` (typ: **Lookup**, `Related table`: `Voivodeship`)
        *   `County` (typ: **Lookup**, `Related table`: `County`)
    4.  Zapisz tabelę.
*   **B. Import Dataflow (`Dataflow_OperatingArea`):**
    1.  Stwórz nowy Dataflow `Dataflow_OperatingArea`.
    2.  Źródło: `firmyobszardzialania.csv`, użyj `Use First Row as Headers`.
    3.  Mapowanie: `Load to existing table` -> `Operating Area`.
        *   `id_firmy` -> `Account` (użyje AK na `Account`)
        *   `id_wojewodztwa` -> `Voivodeship` (użyje AK na `Voivodeship`)
        *   `id_powiaty` -> `County` (użyje AK na `County`)
    4.  `Publish`.

### **4.2. Tabela: `Tender` (z `tenders.csv`)**

*   **A. Ręczne tworzenie tabeli `Tender`:**
    1.  `Display name`: `Tender`, `Plural name`: `Tenders`.
    2.  Kolumny:
        1.  `Legacy Tender ID` (tekst)
        2.  `Received Date` (typ: `Date and Time`)
        3.  **`Status`** (typ: **`Choice`**). Ręcznie dodaj opcje, które znajdziesz w pliku, np. "Złożono", "Anulowano", "Wygrał", "Przegrał".
        4.  `Extracted Content` (tekst wielowierszowy)
        5.  `Account` (typ: **Lookup** do tabeli `Account`)
        6.  `Project` (typ: **Lookup** do tabeli `Project`)
    3.  Zapisz tabelę.
*   **B. AK na `Tender`:** Utwórz AK na kolumnie `Legacy Tender ID`.
*   **C. Dataflow `Dataflow_Tender`:** Źródło `tenders.csv`. Mapowanie do `Tender` (`id` -> `Legacy Tender ID`, `nazwa_oferty` -> `Name`, `data_otrzymania` -> `Received Date`, `status` -> `Status`, `extracted_content` -> `Extracted Content`, `id_firmy` -> `Account` (użyje AK), `id_projektu` -> `Project` (użyje AK)).

### **4.3. Tabela: `Unit Price` (z `unit_prices.csv`)**

*   **A. Tabela `Unit Price`:** `Display name`: `Unit Price`. Kolumny:
    1. `Legacy Unit Price ID` (tekst)
    2. `Unit of Measure` (tekst)
    3. `Price` (typ: `Decimal Number`)
    4. `Notes` (tekst wielowierszowy)
    5. `Tender` (typ: **Lookup** do `Tender`)
    6. `Work Type` (typ: **Lookup** do `Work Type`)
*   **B. AK na `Unit Price`:** Utwórz AK na `Legacy Unit Price ID`.
*   **C. Dataflow `Dataflow_UnitPrice`:** Źródło `unit_prices.csv`. Mapowanie do `Unit Price` (`id` -> `Legacy Unit Price ID`, `jednostka_miary` -> `Unit of Measure`, `cena_jednostkowa` -> `Price`, `uwagi` -> `Notes`, `id_oferty` -> `Tender` (użyje AK), `id_work_type` -> `Work Type` (użyje AK)).

---

## **Grupa 5: Pozostałe tabele danych (Adresy, E-maile, Telefony, Oceny)**

### **5.1. Tabela: `Address` (z `adresy.csv` i `adresy_typ.csv`)**

*   **A. Tabela `Address`:** `Display name`: `Address`. Kolumny:
    1. `Legacy Address ID` (tekst)
    2. `Account` (typ: **Lookup** do `Account`)
    3. `Address Type` (typ: **Choice**). Ręcznie dodaj opcje z pliku `adresy_typ.csv`.
    4. `County` (typ: **Lookup** do `County`)
    5. `Street` (tekst), `City` (tekst), `Postal Code` (tekst).
*   **B. Dataflow `Dataflow_Address`:**
    1. Zapytanie `adresy` (z `adresy.csv`) i `adresy_typ` (z `adresy_typ.csv`). Ujednolić typy kluczy do scalenia (`id_adres_typ` i `id`) na `Whole Number`.
    2. Scal `adresy` z `adresy_typ` po kluczu typu adresu, aby uzyskać jego nazwę.
    3. Mapowanie do `Address`: `id` -> `Legacy Address ID`, `id_firmy` -> `Account` (użyje AK), `id_powiaty` -> `County` (użyje AK), `nazwa` (ze scalenia) -> `Address Type`, `ulica` -> `Street`, `miasto` -> `City`, `kod_pocztowy` -> `Postal Code`.
    4. Ustaw zapytanie `adresy_typ` na `Do not load`.

### **5.2. Tabela: `Email` (z `email.csv` i `email_typ.csv`)**

*   **A. Tabela `Email`:** `Display name`: `Email`. Kolumny:
    1. `Legacy Email ID` (tekst)
    2. `Account` (typ: **Lookup** do `Account`)
    3. `Email Type` (typ: **Choice**). Ręcznie dodaj opcje z pliku `email_typ.csv`.
    4. `Email Address` (tekst).
*   **B. Dataflow `Dataflow_Email`:**
    1. Zapytanie `email` i `email_typ`. Ujednolić typy kluczy do scalenia.
    2. Scal, aby uzyskać nazwę typu e-maila.
    3. Mapowanie do `Email`: `id` -> `Legacy Email ID`, `id_firmy` -> `Account` (użyje AK), `nazwa` (ze scalenia) -> `Email Type`, `email` -> `Email Address`.
    4. Ustaw `email_typ` na `Do not load`.

### **5.3. Tabela: `Phone` (z `telefon.csv` i `telefon_typ.csv`)**

*   **A. Tabela `Phone`:** `Display name`: `Phone`. Kolumny:
    1. `Legacy Phone ID` (tekst)
    2. `Account` (typ: **Lookup** do `Account`)
    3. `Phone Type` (typ: **Choice**). Ręcznie dodaj opcje z pliku `telefon_typ.csv`.
    4. `Phone Number` (tekst).
*   **B. Dataflow `Dataflow_Phone`:**
    1. Zapytanie `telefon` i `telefon_typ`. Ujednolić typy kluczy do scalenia.
    2. Scal, aby uzyskać nazwę typu telefonu.
    3. Mapowanie do `Phone`: `id` -> `Legacy Phone ID`, `id_firmy` -> `Account` (użyje AK), `nazwa` (ze scalenia) -> `Phone Type`, `telefon` -> `Phone Number`.
    4. Ustaw `telefon_typ` na `Do not load`.

### **5.4. Tabela: `Rating` (z `oceny.csv`)**

*   **A. Tabela `Rating`:** `Display name`: `Rating`. Kolumny:
    1. `Legacy Rating ID` (tekst)
    2. `Account` (typ: **Lookup** do `Account`)
    3. `Rating Value` (typ: `Whole Number`)
    4. `Notes` (tekst wielowierszowy).
*   **B. Dataflow `Dataflow_Rating`:** Źródło `oceny.csv`. Mapowanie do `Rating` (`id` -> `Legacy Rating ID`, `id_firmy` -> `Account` (użyje AK), `ocena` -> `Rating Value`, `uwagi` -> `Notes`).

---

## **Grupa 6: Przypadek specjalny: Relacja Wiele-do-wielu (N:N)**

### **6.1. Relacja `Account` <-> `Specialty` (z `firmyspecjalnosci.csv`)**

*   **Problem:** Dataflows nie potrafią bezpośrednio tworzyć relacji N:N. Plik `firmyspecjalnosci.csv` zawiera pary `id_firmy` i `id_specjalnosci`, które reprezentują tę relację.
*   **Rozwiązanie:** Po zaimportowaniu wszystkich tabel i upewnieniu się, że `Account` i `Specialty` są wypełnione, będziemy musieli użyć **Power Automate** do utworzenia tych powiązań.
    *   Stworzymy prosty przepływ, który odczyta plik `firmyspecjalnosci.csv`.
    *   Dla każdej pary `id_firmy` i `id_specjalnosci`, przepływ wyszuka odpowiednie rekordy `Account` i `Specialty` (używając ich Kluczy Alternatywnych).
    *   Następnie utworzy powiązanie między nimi w tabeli relacji N:N.
*   **Instrukcje do tego kroku zostaną dostarczone, gdy wszystkie inne tabele zostaną zaimportowane.**
