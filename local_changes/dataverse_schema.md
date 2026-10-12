# Model Danych Aplikacji (Dataverse)

**Wersja:** 1.0 (po implementacji importu i logiki obszarów działania)
**Cel:** Dokumentacja techniczna struktury bazy danych w Microsoft Dataverse, przeznaczona dla deweloperów aplikacji.

---

## Legenda
*   **Nazwa Wyświetlana:** Nazwa widoczna dla użytkownika w interfejsie.
*   **Nazwa Schematu:** Wewnętrzna, systemowa nazwa używana w API, Power Automate i kodzie. Zazwyczaj z prefiksem `sub_`.
*   **Typ Danych:** Rodzaj danych przechowywanych w kolumnie (np. Tekst, Liczba, Wyszukiwanie).
*   **Relacja:** Wskazuje na połączenie z inną tabelą.

---

## 1. Tabele Główne (Core Entities)

Podstawowe obiekty w systemie.

### 1.1. Firma (Company)
*   **Nazwa Schematu:** `sub_company`
*   **Opis:** Przechowuje informacje o firmach (podwykonawcach, klientach itp.).

| Nazwa Wyświetlana        | Nazwa Schematu             | Typ Danych        | Opis / Uwagi                                                                                             |
| ------------------------ | -------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------- |
| **Company ID**           | `sub_companyid`            | **Primary Key**   | Unikalny identyfikator GUID rekordu.                                                                       |
| Nazwa firmy              | `sub_name`                 | Tekst             | Główna, wymagana nazwa firmy.                                                                            |
| Legacy Company ID        | `sub_legacycompanytid`     | Tekst             | ID z poprzedniego systemu, używane do importu i mapowania danych. Klucz alternatywny.                    |
| Strona WWW               | `sub_stronawww`            | Tekst (URL)       | Adres strony internetowej firmy.                                                                         |
| Typ firmy                | `sub_typfirmy`             | **Wybór (Choice)**| Zastępuje poprzednią tabelę słownikową. Przechowuje typy takie jak "Podwykonawca", "Dostawca" itp.      |
| **Zakres działania**     | `sub_zakresdzialania`      | **Wybór (Choice)**| **Kluczowa kolumna logiki!** Określa, czy firma działa w "Całej Polsce" czy na "Określonych obszarach". |

### 1.2. Osoba (Contact)
*   **Nazwa Schematu:** `sub_contact`
*   **Opis:** Dane kontaktowe osób powiązanych z firmami.

| Nazwa Wyświetlana | Nazwa Schematu    | Typ Danych        | Opis / Uwagi                               |
| ----------------- | ----------------- | ----------------- | ------------------------------------------ |
| **Contact ID**    | `sub_contactid`   | **Primary Key**   | Unikalny identyfikator GUID rekordu.       |
| Imię i Nazwisko   | `sub_name`        | Tekst             | Pełna nazwa osoby.                         |
| Firma             | `sub_company`     | **Wyszukiwanie**  | **Relacja (1:N)** do tabeli `Company`.     |

---

## 2. Tabele Powiązane z Firmą (Related Data)

Tabele przechowujące szczegółowe informacje, zawsze w kontekście konkretnej firmy.

### 2.1. Adres (Address)
*   **Nazwa Schematu:** `sub_address`

| Nazwa Wyświetlana | Nazwa Schematu    | Typ Danych        | Opis / Uwagi                               |
| ----------------- | ----------------- | ----------------- | ------------------------------------------ |
| **Address ID**    | `sub_addressid`   | **Primary Key**   | Unikalny identyfikator GUID rekordu.       |
| Firma             | `sub_company`     | **Wyszukiwanie**  | **Relacja (1:N)** do tabeli `Company`.     |
| Ulica, miasto itp. | `sub_street`...  | Tekst             | Standardowe pola adresowe.                 |
| Typ adresu        | `sub_addresstype` | **Wybór (Choice)**| Zastępuje tabelę słownikową. Np. "Siedziba", "Adres korespondencyjny". |

### 2.2. Email
*   **Nazwa Schematu:** `sub_email`

| Nazwa Wyświetlana | Nazwa Schematu  | Typ Danych        | Opis / Uwagi                               |
| ----------------- | --------------- | ----------------- | ------------------------------------------ |
| **Email ID**      | `sub_emailid`   | **Primary Key**   | Unikalny identyfikator GUID rekordu.       |
| Firma             | `sub_company`   | **Wyszukiwanie**  | **Relacja (1:N)** do tabeli `Company`.     |
| Adres e-mail      | `sub_emailaddress`| Tekst (Email)     | Adres e-mail.                              |
| Typ e-maila       | `sub_emailtype` | **Wybór (Choice)**| Zastępuje tabelę słownikową. Np. "Służbowy", "Prywatny". |

### 2.3. Telefon (Phone)
*   **Nazwa Schematu:** `sub_phone`

| Nazwa Wyświetlana | Nazwa Schematu  | Typ Danych        | Opis / Uwagi                               |
| ----------------- | --------------- | ----------------- | ------------------------------------------ |
| **Phone ID**      | `sub_phoneid`   | **Primary Key**   | Unikalny identyfikator GUID rekordu.       |
| Firma             | `sub_company`   | **Wyszukiwanie**  | **Relacja (1:N)** do tabeli `Company`.     |
| Numer telefonu    | `sub_phonenumber`| Tekst (Phone)     | Numer telefonu.                            |
| Typ telefonu      | `sub_phonetype` | **Wybór (Choice)**| Zastępuje tabelę słownikową. Np. "Komórkowy", "Stacjonarny". |

---

## 3. Tabele Słownikowe i Biznesowe

Tabele używane do kategoryzacji i definiowania logiki biznesowej.

### 3.1. Kategoria (Category)
*   **Nazwa Schematu:** `sub_category`

### 3.2. Specjalizacja (Specialty)
*   **Nazwa Schematu:** `sub_specialty`
*   **Relacja:** Połączona z `Company` relacją **Wiele-do-wielu (N:N)**.

### 3.3. Województwo (Voivodeship)
*   **Nazwa Schematu:** `sub_voivodeship`

### 3.4. Powiat (County)
*   **Nazwa Schematu:** `sub_county`
*   **Relacja:** Posiada pole **Wyszukiwania** do tabeli `Voivodeship`, tworząc relację 1:N (jedno województwo ma wiele powiatów).

---

## 4. Logika Obszaru Działania

Ten moduł definiuje, gdzie dana firma świadczy swoje usługi.

### 4.1. Tabela: Obszar działania firmy (Company Operating Area)
*   **Nazwa Schematu:** `sub_companyoperatingarea` (lub podobna)
*   **Typ:** Tabela pośrednicząca (Junction Table).
*   **Cel:** Przechowuje szczegółowe definicje obszarów, jeśli w tabeli `Company` wybrano opcję `Zakres działania = Określone obszary`.

| Nazwa Wyświetlana | Nazwa Schematu      | Typ Danych        | Opis / Uwagi                                                              |
| ----------------- | ------------------- | ----------------- | ------------------------------------------------------------------------- |
| **Area ID**       | `sub_...areaid`     | **Primary Key**   | Unikalny identyfikator GUID rekordu.                                      |
| **Firma**         | `sub_company`       | **Wyszukiwanie**  | **(Wymagane)** Wskazuje na firmę, której dotyczy ten wpis.                |
| **Województwo**   | `sub_voivodeship`   | **Wyszukiwanie**  | (Opcjonalne) Wskazuje na całe województwo.                                 |
| **Powiat**        | `sub_county`        | **Wyszukiwanie**  | (Opcjonalne) Wskazuje na konkretny powiat.                                |

### 4.2. Logika działania w aplikacji

1.  **Sprawdź pole `sub_zakresdzialania` w tabeli `Company`:**
    *   Jeśli wartość to **`Cała Polska`**: Ignoruj tabelę `Obszar działania firmy`. Firma działa wszędzie.
    *   Jeśli wartość to **`Określone obszary`**: Przejdź do kroku 2.

2.  **Odczytaj rekordy z tabeli `Obszar działania firmy` dla danej firmy:**
    *   Dla każdego rekordu sprawdź:
        *   Jeśli pole `Województwo` jest wypełnione, a `Powiat` jest **puste**: Firma działa na terenie **całego** wskazanego województwa.
        *   Jeśli pole `Powiat` jest wypełnione: Firma działa na terenie wskazanego powiatu. (Aplikacja może dodatkowo wyświetlić, z jakiego województwa jest ten powiat, pobierając dane z relacji Powiat -> Województwo).

3.  **Prezentacja:** Aplikacja powinna zagregować te dane i przedstawić użytkownikowi pełną listę obszarów, np.:
    *   Województwo Mazowieckie (całe)
    *   Województwo Pomorskie (Powiat gdański, Powiat starogardzki)
    *   Województwo Małopolskie (całe)