# Instrukcja Odtworzenia Aplikacji dla LLM

Ta instrukcja opisuje logikę i strukturę aplikacji do zarządzania bazą firm, ofert i analizy cen jednostkowych. Celem jest odtworzenie **funkcjonalności** aplikacji, pomijając aspekty wizualne i konkretny język programowania.

## 1. Struktura Danych (Modele)

Aplikacja opiera się na następujących głównych encjach i relacjach między nimi:

### A. Encje Główne

- **Firma (Company)**: Centralny obiekt w systemie.
    - Atrybuty: Nazwa, Typ (np. Generalny Wykonawca, Podwykonawca), Strona WWW, Uwagi.
    - Relacje:
        - Ma wiele **Adresów**.
        - Ma wiele **Emaili**.
        - Ma wiele **Telefonów**.
        - Ma wiele **Osób Kontaktowych**.
        - Ma wiele **Ocen**.
        - Ma wiele **Specjalności** (relacja wiele-do-wielu).
        - Ma wiele **Obszarów Działania** (relacja wiele-do-wielu).
        - Może złożyć wiele **Ofert**.

- **Oferta (Tender)**: Reprezentuje ofertę złożoną przez firmę.
    - Atrybuty: Nazwa oferty, Data otrzymania, Status (np. Nowa, Zakończona), Nazwa oryginalnego pliku, Ścieżka do pliku w systemie przechowywania, Typ pliku, Wyekstrahowana treść (duże pole tekstowe).
    - Relacje:
        - Należy do jednej **Firmy**.
        - Należy do jednego **Projektu**.
        - Ma wiele **Cen Jednostkowych**.

- **Cena Jednostkowa (UnitPrice)**: Konkretna pozycja w ofercie.
    - Atrybuty: Jednostka miary, Cena, Uwagi.
    - Relacje:
        - Należy do jednej **Oferty**.
        - Należy do jednego **Rodzaju Roboty**.
        - Należy do jednej **Kategorii**.

- **Projekt (Project)**: Reprezentuje budowę lub zadanie, którego dotyczy oferta.
    - Atrybuty: Nazwa projektu, Skrót, Rodzaj, Uwagi.
    - Relacje:
        - Ma wiele **Ofert**.

- **Rodzaj Roboty (WorkType)**: Słownik definujący typy prac (np. "Ściany żelbetowe", "Tynki gipsowe").
    - Atrybuty: Nazwa.
    - Relacje:
        - Należy do jednej **Kategorii**.
        - Ma wiele **Cen Jednostkowych**.

- **Kategoria (Category)**: Słownik grupujący `Rodzaje Robót` (np. "Roboty żelbetowe", "Roboty wykończeniowe").
    - Atrybuty: Nazwa.
    - Relacje:
        - Ma wiele **Rodzajów Robót**.
        - Ma wiele **Cen Jednostkowych**.

### B. Encje Pomocnicze i Słownikowe

- **Osoba Kontaktowa (Person)**: Pracownik firmy.
    - Atrybuty: Imię, Nazwisko, Stanowisko, Email, Telefon.
    - Relacje: Należy do jednej **Firmy**.

- **Ocena (Rating)**: Ocena współpracy z firmą.
    - Atrybuty: Osoba oceniająca, Rok współpracy, Ocena (np. 1-5), Komentarz.
    - Relacje: Należy do jednej **Firmy**.

- **Adres (Address)**, **Email**, **Telefon**: Dane kontaktowe firmy. Każdy z nich ma swój typ (np. adres 'siedziby', 'korespondencyjny').
    - Relacje: Należą do jednej **Firmy**.

- **Specjalność (Specialty)**: Słownik specjalności firm (np. "Instalacje sanitarne").

- **Obszar Działania (Area of Operation)**: Definiuje geograficzny zasięg firmy. Jest to model łączący **Firmę** z **Krajem**, **Województwem** i **Powiatem**.

- **Typy (FirmyTyp, AdresyTyp, EmailTyp, TelefonTyp)**: Tabele słownikowe dla typów firm, adresów, emaili i telefonów.

## 2. Logika Aplikacji i Funkcjonalności

### A. Zarządzanie Danymi (CRUD)

- Implementacja pełnych operacji CRUD (Create, Read, Update, Delete) dla wszystkich głównych i słownikowych encji wymienionych powyżej.
- Formularze do tworzenia i edycji powinny obsługiwać wszystkie pola i relacje (np. formularz firmy pozwala na dynamiczne dodawanie/usuwanie adresów, osób kontaktowych, ocen itd.).


### C. Wyszukiwanie i Filtrowanie Firm

- Stworzenie zaawansowanej funkcji wyszukiwania firm, która przeszukuje znormalizowany tekst (unidecode, małe litery) we wszystkich polach **Firmy** oraz polach jej powiązanych obiektów (Adresy, Emaile, Telefony, Osoby, Oceny, Specjalności, Obszary Działania).
- Implementacja filtrowania listy firm na podstawie:
    - **Specjalności** (wiele opcji do wyboru).
    - **Obszaru Działania**:
        - Wybór województwa powinien pokazywać firmy działające w tym województwie oraz te o zasięgu ogólnokrajowym.
        - Wybór powiatu powinien pokazywać firmy działające w tym powiecie, w całym województwie, do którego należy powiat, oraz te o zasięgu ogólnokrajowym.
    - **Typu Firmy** (wiele opcji do wyboru).

### D. Zarządzanie Ofertami (Tenders)

- **Upload Plików**:
    - Użytkownik może wgrać plik oferty (PDF, XLSX, XLS) podczas tworzenia lub edycji **Oferty**.
    - Plik musi być przechowywany w bezpiecznym miejscu (np. system plików lub usługa chmury jak Google Cloud Storage).

    - Na specjalnym widoku , użytkownik widzi podgląd treść oferty.
    - Na tym samym widoku znajduje się formularz do ręcznego dodawania **Cen Jednostkowych** na podstawie odczytanej treści.
    - Formularz powinien pozwalać na wybranie **Rodzaju Roboty** z listy (z opcją dodania nowego rodzaju w locie) i automatyczne przypisanie **Kategorii** na podstawie wybranego rodzaju roboty.

### E. Analiza Cen Jednostkowych

Stworzenie dedykowanych widoków do analizy zgromadzonych danych o cenach.

- **Globalna Lista Cen Jednostkowych**: Tabela wszystkich cen z opcjami filtrowania po rodzaju roboty, kategorii, ofercie, firmie i projekcie.
- **Porównanie Cen (Analysis View)**:
    - Widok tabelaryczny, gdzie wiersze to **Rodzaje Robót**, a kolumny to wybrane **Oferty**. Komórki tabeli pokazują cenę jednostkową dla danej roboty w danej ofercie.
    - Opcje filtrowania:
        - Po **Kategorii** (ogranicza listę rodzajów robót).
        - Po **Ofertach** (pozwala wybrać, które oferty porównujemy).
        - Po dacie i statusie ofert.
- **Pulpit Analityczny (Dashboard)**:
    - Użytkownik wybiera jeden **Rodzaj Roboty**.
    - System wyświetla statystyki (min, max, średnia, mediana) dla cen tego rodzaju roboty.
    - Dane do statystyk można filtrować po dacie i statusie ofert. Użytkownik może ręcznie zaznaczać/odznaczać poszczególne pozycje cenowe, które mają być wliczane do analizy.
    - **Wykresy**:
        1. **Ewolucja Ceny w Czasie**: Wykres liniowy pokazujący średnią cenę w kolejnych miesiącach/latach.
        2. **Porównanie Wykonawców**: Wykres słupkowy pokazujący średnią cenę oferowaną przez każdą z firm.
        3. **Rozkład Cen**: Histogram pokazujący, w jakich przedziałach cenowych najczęściej pojawiały się oferty.
        4. **Sezonowość**: Wykres pokazujący średnią cenę w poszczególnych miesiącach roku (np. średnia cena ze wszystkich styczniów, lutych itd.).
        5. **Konkurencyjność Wykonawców**: Wykres pokazujący min, max i średnią cenę dla każdego wykonawcy.
