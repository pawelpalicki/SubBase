# Kompletna i Ostateczna Instrukcja Importu Danych do Dataverse

**Uwaga:** Ta instrukcja zastępuje wszystkie poprzednie dokumenty (`plan_importu_danych.md`, `Migracja_Power_App_Instrukcje.md`, `instrukcja_importu_osob.md`) i jest jedyną aktualną wersją. Proszę postępować **dokładnie** według poniższej kolejności.

## Wprowadzenie

Proces importu musi odbywać się w określonej kolejności ze względu na relacje (powiązania) między tabelami. Tabele podstawowe (słownikowe) muszą zostać zaimportowane przed tabelami, które z nich korzystają. Poniżej znajduje się lista plików `.csv` w **obowiązującej kolejności importu**.

Podczas importu każdej tabeli w Power Apps, kluczowe jest prawidłowe zmapowanie kolumn, a w szczególności pól typu **Lookup (odnośnik)**, które tworzą relacje między danymi.

---

## Etap 1: Tabele Słownikowe (Dane Podstawowe)

Te tabele nie mają zależności od innych i muszą zostać zaimportowane jako pierwsze.

1.  **`adresy_typ.csv`** (Tabela: `AdresyTyp`)
    *   Opis: Definiuje typy adresów (np. siedziba, korespondencyjny).
    *   Mapowanie: Standardowe.

2.  **`categories.csv`** (Tabela: `Category`)
    *   Opis: Główne kategorie dla robót budowlanych.
    *   Mapowanie: Standardowe.

3.  **`email_typ.csv`** (Tabela: `EmailTyp`)
    *   Opis: Definiuje typy adresów e-mail.
    *   Mapowanie: Standardowe.

4.  **`firmy_typ.csv`** (Tabela: `FirmyTyp`)
    *   Opis: Definiuje typy firm (np. podwykonawca, dostawca).
    *   Mapowanie: Standardowe.

5.  **`kraj.csv`** (Tabela: `Kraj`)
    *   Opis: Lista krajów.
    *   Mapowanie: Standardowe.

6.  **`projects.csv`** (Tabela: `Project`)
    *   Opis: Lista projektów/budów.
    *   Mapowanie: Standardowe.

7.  **`specjalnosci.csv`** (Tabela: `Specjalnosci`)
    *   Opis: Lista specjalności firm.
    *   Mapowanie: Standardowe.

8.  **`telefon_typ.csv`** (Tabela: `TelefonTyp`)
    *   Opis: Definiuje typy numerów telefonów.
    *   Mapowanie: Standardowe.

9.  **`wojewodztwa.csv`** (Tabela: `Wojewodztwa`)
    *   Opis: Lista województw.
    *   Mapowanie: Standardowe.

---

## Etap 2: Tabele Zależne (Poziom 1)

Te tabele zależą od danych zaimportowanych w Etapie 1.

10. **`firmy.csv`** (Tabela: `Firmy`)
    *   Opis: Główna lista firm.
    *   **Mapowanie Lookup:**
        *   Kolumna `id_firmy_typ` musi być zmapowana jako **odnośnik** do tabeli `FirmyTyp`.

11. **`powiaty.csv`** (Tabela: `Powiaty`)
    *   Opis: Lista powiatów.
    *   **Mapowanie Lookup:**
        *   Kolumna `id_wojewodztwa` musi być zmapowana jako **odnośnik** do tabeli `Wojewodztwa`.

12. **`work_types.csv`** (Tabela: `WorkType`)
    *   Opis: Rodzaje robót.
    *   **Mapowanie Lookup:**
        *   Kolumna `id_kategorii` musi być zmapowana jako **odnośnik** do tabeli `Category`.

---

## Etap 3: Tabele Zależne (Poziom 2) - Dane powiązane z Firmami

Te tabele zależą głównie od zaimportowanej tabeli `Firmy`.

13. **`adresy.csv`** (Tabela: `Adresy`)
    *   Opis: Adresy przypisane do firm.
    *   **Mapowanie Lookup:**
        *   `id_firmy` -> **odnośnik** do tabeli `Firmy`.
        *   `id_adresy_typ` -> **odnośnik** do tabeli `AdresyTyp`.

14. **`email.csv`** (Tabela: `Email`)
    *   Opis: E-maile przypisane do firm.
    *   **Mapowanie Lookup:**
        *   `id_firmy` -> **odnośnik** do tabeli `Firmy`.
        *   `id_email_typ` -> **odnośnik** do tabeli `EmailTyp`.

15. **`oceny.csv`** (Tabela: `Oceny`)
    *   Opis: Oceny wystawione firmom.
    *   **Mapowanie Lookup:**
        *   `id_firmy` -> **odnośnik** do tabeli `Firmy`.

16. **`osoby.csv`** (Tabela: `Osoby`)
    *   Opis: Osoby kontaktowe w firmach.
    *   **Mapowanie Lookup:**
        *   `id_firmy` -> **odnośnik** do tabeli `Firmy`.

17. **`telefon.csv`** (Tabela: `Telefon`)
    *   Opis: Telefony przypisane do firm.
    *   **Mapowanie Lookup:**
        *   `id_firmy` -> **odnośnik** do tabeli `Firmy`.
        *   `id_telefon_typ` -> **odnośnik** do tabeli `TelefonTyp`.

18. **`tenders.csv`** (Tabela: `Tender`)
    *   Opis: Oferty otrzymane od firm.
    *   **Mapowanie Lookup:**
        *   `id_firmy` -> **odnośnik** do tabeli `Firmy`.
        *   `id_projektu` -> **odnośnik** do tabeli `Project`.

---

## Etap 4: Tabele Łączące (Wiele-do-wielu)

Te tabele tworzą złożone relacje między danymi.

19. **`firmyspecjalnosci.csv`** (Tabela: `FirmySpecjalnosci`)
    *   Opis: Łączy firmy z ich specjalnościami.
    *   **Mapowanie Lookup:**
        *   `id_firmy` -> **odnośnik** do tabeli `Firmy`.
        *   `id_specjalnosci` -> **odnośnik** do tabeli `Specjalnosci`.

20. **`firmyobszardzialania.csv`** (Tabela: `FirmyObszarDzialania`)
    *   Opis: Określa obszar działania firm.
    *   **Mapowanie Lookup:**
        *   `id_firmy` -> **odnośnik** do tabeli `Firmy`.
        *   `id_kraj` -> **odnośnik** do tabeli `Kraj`.
        *   `id_wojewodztwa` -> **odnośnik** do tabeli `Wojewodztwa`.
        *   `id_powiaty` -> **odnośnik** do tabeli `Powiaty`.

---

## Etap 5: Tabela Zależna (Poziom 3) - Dane powiązane z Ofertami

Ostatnia tabela, która zależy od danych z poprzednich etapów.

21. **`unit_prices.csv`** (Tabela: `UnitPrice`)
    *   Opis: Ceny jednostkowe w ofertach.
    *   **Mapowanie Lookup:**
        *   `id_oferty` -> **odnośnik** do tabeli `Tender`.
        *   `id_work_type` -> **odnośnik** do tabeli `WorkType`.
        *   `id_kategorii` -> **odnośnik** do tabeli `Category`.

---
Proszę o ścisłe przestrzeganie tej kolejności, aby zapewnić integralność danych po imporcie.
