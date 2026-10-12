# Instrukcja Importu Osób do Dataverse

Ta instrukcja opisuje, jak poprawnie zaimportować dane osób (`osoby`) i połączyć je z istniejącymi firmami (`firmy`) w Dataverse.

## Krok 1: Przygotowanie pliku `osoby.csv`

Przed importem upewnij się, że Twój plik `osoby.csv` zawiera następujące kolumny:

- `id_osoby`: Unikalny identyfikator każdej osoby.
- `imie`: Imię osoby.
- `nazwisko`: Nazwisko osoby.
- `stanowisko`: Stanowisko służbowe.
- `e_mail`: Adres e-mail.
- `telefon`: Numer telefonu.
- `id_firmy`: **Kluczowe pole!** Jest to identyfikator firmy z tabeli `firmy`, do której dana osoba jest przypisana. Upewnij się, że dla każdej osoby istnieje odpowiedni wpis `id_firmy` w tym pliku.

**Przykład struktury pliku `osoby.csv`:**
```csv
id_osoby,imie,nazwisko,stanowisko,e_mail,telefon,id_firmy
1,Jan,Kowalski,Dyrektor,j.kowalski@przyklad.com,123456789,101
2,Anna,Nowak,Specjalista,a.nowak@przyklad.com,987654321,102
3,Piotr,Zieliński,Manager,p.zielinski@przyklad.com,555444333,101
```

## Krok 2: Import danych w Power Apps

1. Przejdź do Power Apps i wybierz tabelę `Osoby`.
2. Użyj opcji "Importuj dane z pliku" i wybierz przygotowany plik `osoby.csv`.
3. Rozpocznie się proces mapowania kolumn.

## Krok 3: Mapowanie kolumn

System powinien automatycznie zmapować większość kolumn. Zwróć szczególną uwagę na następujące mapowania:

- **Imię** -> `imie`
- **Nazwisko** -> `nazwisko`
- **Stanowisko** -> `stanowisko`
- **E-mail** -> `e_mail`
- **Telefon** -> `telefon`

### Mapowanie relacji z firmą (Najważniejszy krok)

To jest kluczowy moment, w którym łączysz importowane osoby z istniejącymi firmami.

- Dla kolumny `id_firmy` z Twojego pliku CSV, musisz ustawić **relację odnośnika (lookup)** do tabeli `Firmy`.
- W polu docelowym wybierz kolumnę, która jest kluczem głównym w tabeli `Firmy` (prawdopodobnie `id_firmy` lub `Firmy ID`).

Dzięki temu system połączy każdą osobę z odpowiednią firmą na podstawie `id_firmy`.

## Krok 4: Zakończenie importu

Po poprawnym zmapowaniu wszystkich kolumn, zakończ proces importu. System zaimportuje dane osób i automatycznie powiąże je z firmami.

---
**Uwaga:** Jeśli któraś z instrukcji w plikach `plan_importu_danych.md` lub `Migracja_Power_App_Instrukcje.md` jest sprzeczna z tą instrukcją, proszę kierować się **tą instrukcją**, ponieważ została ona zweryfikowana z aktualną strukturą bazy danych aplikacji.
