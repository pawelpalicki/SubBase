from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import (
    Firmy, FirmyTyp, Adresy, Email, Telefon, Osoby, Oceny,
    Specjalnosci, FirmySpecjalnosci, Wojewodztwa, Powiaty, Kraj,
    FirmyObszarDzialania, AdresyTyp, EmailTyp, TelefonTyp
)
from app.utils import normalize_text
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError
from . import main

# --- Helper Functions ---

def get_filtered_companies_query():
    """Wspólna logika filtrowania firm dla listy i eksportu."""
    query = Firmy.query
    
    # Handle search filter
    search = request.args.get('search', '')
    if search:
        # Normalizacja tekstu wyszukiwania
        normalized_search = normalize_text(search)
        matching_company_ids = set()

        # Wyszukiwanie w tabeli FIRMY
        firmy_results = Firmy.query.all()
        for firma in firmy_results:
            if (normalized_search in normalize_text(firma.nazwa_firmy).lower() or
                normalized_search in normalize_text(firma.strona_www).lower() or
                normalized_search in normalize_text(firma.uwagi).lower()):
                matching_company_ids.add(firma.id_firmy)

        # Helper do przeszukiwania powiązanych tabel
        def search_related(model, fields, id_field='id_firmy'):
            results = model.query.all()
            for item in results:
                match = False
                for field in fields:
                    val = getattr(item, field)
                    if normalized_search in normalize_text(val).lower():
                        match = True
                        break
                if match:
                    company_id = getattr(item, id_field)
                    if company_id:
                        matching_company_ids.add(company_id)

        search_related(Adresy, ['kod', 'miejscowosc', 'ulica_miejscowosc'])
        search_related(Email, ['e_mail'])
        search_related(Telefon, ['telefon'])
        search_related(Osoby, ['imie', 'nazwisko', 'stanowisko', 'e_mail', 'telefon'])
        search_related(Oceny, ['osoba_oceniajaca', 'budowa_dzial', 'komentarz'])

        # Specjalności
        specjalnosci_results = Specjalnosci.query.all()
        for spec in specjalnosci_results:
            if normalized_search in normalize_text(spec.specjalnosc).lower():
                firmy_spec = FirmySpecjalnosci.query.filter_by(id_specjalnosci=spec.id_specjalnosci).all()
                for fs in firmy_spec:
                    matching_company_ids.add(fs.id_firmy)

        # Typy firm
        firmy_typ_results = FirmyTyp.query.all()
        for typ in firmy_typ_results:
            if normalized_search in normalize_text(typ.typ_firmy).lower():
                firmy_by_typ = Firmy.query.filter_by(id_firmy_typ=typ.id_firmy_typ).all()
                for firma in firmy_by_typ:
                    matching_company_ids.add(firma.id_firmy)

        # Obszary działania
        wojewodztwa_results = Wojewodztwa.query.all()
        for woj in wojewodztwa_results:
            if normalized_search in normalize_text(woj.wojewodztwo).lower():
                firmy_woj = FirmyObszarDzialania.query.filter_by(id_wojewodztwa=woj.id_wojewodztwa).all()
                for fw in firmy_woj:
                    matching_company_ids.add(fw.id_firmy)

        powiaty_results = Powiaty.query.all()
        for pow in powiaty_results:
            if normalized_search in normalize_text(pow.powiat).lower():
                firmy_pow = FirmyObszarDzialania.query.filter_by(id_powiaty=pow.id_powiaty).all()
                for fp in firmy_pow:
                    matching_company_ids.add(fp.id_firmy)

        kraje_results = Kraj.query.all()
        for kraj in kraje_results:
            if normalized_search in normalize_text(kraj.kraj).lower():
                firmy_kraj = FirmyObszarDzialania.query.filter_by(id_kraj=kraj.id_kraj).all()
                for fk in firmy_kraj:
                    matching_company_ids.add(fk.id_firmy)

        if matching_company_ids:
            query = query.filter(Firmy.id_firmy.in_(matching_company_ids))
        else:
            query = query.filter(False)

    # Handle specialty filter
    specialties = request.args.getlist('specialties')
    if specialties:
        query = query.join(FirmySpecjalnosci).filter(FirmySpecjalnosci.id_specjalnosci.in_(specialties))

    # Handle area filter
    wojewodztwo = request.args.get('wojewodztwo')
    powiat = request.args.get('powiat')

    if powiat:
        nationwide_companies = db.session.query(Firmy.id_firmy).join(FirmyObszarDzialania).filter(FirmyObszarDzialania.id_kraj == 'POL')
        powiat_data = Powiaty.query.filter_by(id_powiaty=powiat).first()

        if powiat_data:
            wojewodztwo_id = powiat_data.id_wojewodztwa
            powiat_companies = db.session.query(Firmy.id_firmy).join(FirmyObszarDzialania).filter(FirmyObszarDzialania.id_powiaty == powiat)
            wojewodztwo_empty_powiat_companies = db.session.query(Firmy.id_firmy).join(FirmyObszarDzialania).filter(and_(FirmyObszarDzialania.id_wojewodztwa == wojewodztwo_id, FirmyObszarDzialania.id_powiaty == 0))
            combined_companies = nationwide_companies.union(powiat_companies, wojewodztwo_empty_powiat_companies).subquery()
        else:
            combined_companies = nationwide_companies.subquery()

        query = query.filter(Firmy.id_firmy.in_(combined_companies))

    elif wojewodztwo and not powiat:
        nationwide_companies = db.session.query(Firmy.id_firmy).join(FirmyObszarDzialania).filter(FirmyObszarDzialania.id_kraj == 'POL')
        wojewodztwo_companies = db.session.query(Firmy.id_firmy).join(FirmyObszarDzialania).filter(FirmyObszarDzialania.id_wojewodztwa == wojewodztwo).filter(FirmyObszarDzialania.id_powiaty == 0).except_(
                                     db.session.query(Firmy.id_firmy).join(FirmyObszarDzialania).filter(FirmyObszarDzialania.id_wojewodztwa == wojewodztwo).filter(FirmyObszarDzialania.id_powiaty != 0)
                                 )
        combined_companies_ids_subquery = nationwide_companies.union(wojewodztwo_companies).subquery()
        query = query.filter(Firmy.id_firmy.in_(combined_companies_ids_subquery))

    # Handle company type filter
    company_types = [ct for ct in request.args.getlist('company_types') if ct.strip()]
    if company_types:
        query = query.filter(Firmy.id_firmy_typ.in_(company_types))
        
    return query

# --- Routes ---

@main.route('/companies')
@login_required 
def list_companies():
    query = get_filtered_companies_query()
    companies = query.all()

    # Get all data needed for filters (dropdowns)
    all_specialties = Specjalnosci.query.all()
    all_wojewodztwa = Wojewodztwa.query.all()
    all_powiaty = Powiaty.query.all()
    all_company_types = FirmyTyp.query.all()

    return render_template('index.html', 
                           companies=companies,
                           all_specialties=all_specialties,
                           all_wojewodztwa=all_wojewodztwa,
                           all_powiaty=all_powiaty,
                           all_company_types=all_company_types,
                           title='Lista Firm')

@main.route('/export_companies_html')
def export_companies_html():
    query = get_filtered_companies_query()
    filtered_companies = query.all()

    # --- Fetch ALL related data for filtered companies ---
    company_ids = [c.id_firmy for c in filtered_companies]
    related_data = {}
    
    if company_ids:
        related_data['adresy'] = db.session.query(Adresy).filter(Adresy.id_firmy.in_(company_ids)).all()
        related_data['emails'] = db.session.query(Email).filter(Email.id_firmy.in_(company_ids)).all()
        related_data['telefony'] = db.session.query(Telefon).filter(Telefon.id_firmy.in_(company_ids)).all()
        related_data['osoby'] = db.session.query(Osoby).filter(Osoby.id_firmy.in_(company_ids)).all()
        related_data['oceny'] = db.session.query(Oceny).filter(Oceny.id_firmy.in_(company_ids)).all()
        related_data['obszary'] = db.session.query(FirmyObszarDzialania).filter(FirmyObszarDzialania.id_firmy.in_(company_ids)).all()
        related_data['specjalnosci'] = db.session.query(FirmySpecjalnosci).filter(FirmySpecjalnosci.id_firmy.in_(company_ids)).all()

        # Lookup details
        specialty_ids = list(set([fs.id_specjalnosci for fs in related_data.get('specjalnosci', []) if fs.id_specjalnosci]))
        if specialty_ids:
             related_data['specialty_details'] = {s.id_specjalnosci: s for s in db.session.query(Specjalnosci).filter(Specjalnosci.id_specjalnosci.in_(specialty_ids)).all()}
        else:
             related_data['specialty_details'] = {}

        woj_ids = list(set([fo.id_wojewodztwa for fo in related_data.get('obszary', []) if fo.id_wojewodztwa]))
        powiat_ids = list(set([fo.id_powiaty for fo in related_data.get('obszary', []) if fo.id_powiaty]))
        
        if woj_ids:
            related_data['wojewodztwa_details'] = {w.id_wojewodztwa: w for w in db.session.query(Wojewodztwa).filter(Wojewodztwa.id_wojewodztwa.in_(woj_ids)).all()}
        else:
             related_data['wojewodztwa_details'] = {}
             
        if powiat_ids:
            related_data['powiaty_details'] = {p.id_powiaty: p for p in db.session.query(Powiaty).filter(Powiaty.id_powiaty.in_(powiat_ids)).all()}
        else:
             related_data['powiaty_details'] = {}

    # Organize related data by company ID
    organized_related_data = {company.id_firmy: {} for company in filtered_companies}
    for data_type, items in related_data.items():
         if '_details' in data_type: 
             organized_related_data[data_type] = items
         else:
            for item in items:
                if item.id_firmy not in organized_related_data:
                     organized_related_data[item.id_firmy] = {}
                if data_type not in organized_related_data[item.id_firmy]:
                     organized_related_data[item.id_firmy][data_type] = []
                organized_related_data[item.id_firmy][data_type].append(item)

    # Dynamic title generation
    title_parts = []
    search = request.args.get('search', '')
    if search:
        title_parts.append(f"Wyniki wyszukiwania dla: '{search}'")

    specialties = request.args.getlist('specialties')
    if specialties:
        specialty_names = [s.specjalnosc for s in Specjalnosci.query.filter(Specjalnosci.id_specjalnosci.in_(specialties)).all()]
        title_parts.append(f"Specjalności: {', '.join(specialty_names)}")

    powiat = request.args.get('powiat')
    wojewodztwo = request.args.get('wojewodztwo')
    
    if powiat:
        powiat_data = Powiaty.query.filter_by(id_powiaty=powiat).first()
        if powiat_data:
            title_parts.append(f"Powiat: {powiat_data.powiat}")
    elif wojewodztwo:
        wojewodztwo_data = Wojewodztwa.query.filter_by(id_wojewodztwa=wojewodztwo).first()
        if wojewodztwo_data:
            title_parts.append(f"Województwo: {wojewodztwo_data.wojewodztwo}")

    company_types = [ct for ct in request.args.getlist('company_types') if ct.strip()]
    if company_types:
        type_names = [t.typ_firmy for t in FirmyTyp.query.filter(FirmyTyp.id_firmy_typ.in_(company_types)).all()]
        title_parts.append(f"Typy firm: {', '.join(type_names)}")

    if title_parts:
        title = "Lista firm dla filtrów: " + "; ".join(title_parts)
    else:
        title = "Lista wszystkich wyeksportowanych firm"

    return render_template('export_companies_html.html',
                           companies=filtered_companies,
                           related_data=organized_related_data,
                           title=title)

@main.route('/company/<int:company_id>')
def company_details(company_id):
    company = Firmy.query.get_or_404(company_id)

    avg_rating = db.session.query(func.avg(Oceny.ocena)).filter(Oceny.id_firmy == company_id).scalar() or 0
    avg_rating = round(avg_rating, 1)

    nationwide = db.session.query(FirmyObszarDzialania).filter(FirmyObszarDzialania.id_firmy == company_id, FirmyObszarDzialania.id_kraj == 'POL').first() is not None

    wojewodztwa = db.session.query(Wojewodztwa).join(FirmyObszarDzialania).filter(FirmyObszarDzialania.id_firmy == company_id, Wojewodztwa.wojewodztwo != 'Nie dotyczy / Brak danych').all()

    powiaty = db.session.query(Powiaty, Wojewodztwa.id_wojewodztwa).join(FirmyObszarDzialania, Powiaty.id_powiaty == FirmyObszarDzialania.id_powiaty).join(Wojewodztwa, Powiaty.id_wojewodztwa == Wojewodztwa.id_wojewodztwa).filter(FirmyObszarDzialania.id_firmy == company_id).all()

    specialties = db.session.query(Specjalnosci).join(FirmySpecjalnosci).filter(FirmySpecjalnosci.id_firmy == company_id).all()

    is_ajax = request.args.get('ajax', False)

    return render_template('company_details.html',
                            company=company,
                            avg_rating=avg_rating,
                            nationwide=nationwide,
                            wojewodztwa=wojewodztwa,
                            powiaty=powiaty,
                            specialties=specialties,
                            standalone=not is_ajax)

@main.route('/company/new', methods=['GET', 'POST'])
def new_company():
    from app.forms import CompanyForm
    form = CompanyForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Create new company
            company = Firmy(
                nazwa_firmy=form.nazwa_firmy.data,
                id_firmy_typ=form.typ_firmy.data,
                strona_www=form.strona_www.data,
                uwagi=form.uwagi.data
            )
            db.session.add(company)
            db.session.flush()

            with db.session.no_autoflush: # Prevent premature flush
                # Add addresses
                for address_form in form.adresy:
                    if address_form.miejscowosc.data:
                        address = Adresy(
                            kod=address_form.kod.data,
                            miejscowosc=address_form.miejscowosc.data,
                            ulica_miejscowosc=address_form.ulica_miejscowosc.data,
                            id_adresy_typ=address_form.typ_adresu.data,
                            id_firmy=company.id_firmy
                        )
                        db.session.add(address)

                # Add emails
                for email_form in form.emaile:
                    if email_form.email.data:
                        email = Email(
                            e_mail=email_form.email.data,
                            id_email_typ=email_form.typ_emaila.data,
                            id_firmy=company.id_firmy
                        )
                        db.session.add(email)

                # Add phones
                for phone_form in form.telefony:
                    if phone_form.telefon.data:
                        phone = Telefon(
                            telefon=phone_form.telefon.data,
                            id_telefon_typ=phone_form.typ_telefonu.data,
                            id_firmy=company.id_firmy
                        )
                        db.session.add(phone)

                # Add people
                for person_form in form.osoby:
                    if person_form.imie.data and person_form.nazwisko.data:
                        person = Osoby(
                            imie=person_form.imie.data,
                            nazwisko=person_form.nazwisko.data,
                            stanowisko=person_form.stanowisko.data,
                            e_mail=person_form.email.data,
                            telefon=person_form.telefon.data,
                            id_firmy=company.id_firmy
                        )
                        db.session.add(person)

                # Add ratings
                for rating_form in form.oceny:
                    if rating_form.osoba_oceniajaca.data:
                        rating = Oceny(
                            osoba_oceniajaca=rating_form.osoba_oceniajaca.data,
                            budowa_dzial=rating_form.budowa_dzial.data,
                            rok_wspolpracy=rating_form.rok_wspolpracy.data,
                            ocena=rating_form.ocena.data,
                            komentarz=rating_form.komentarz.data,
                            id_firmy=company.id_firmy
                        )
                        db.session.add(rating)

                # Obszar działania
                obszar_type = form.obszar_dzialania.data
                if obszar_type == 'kraj':
                        if form.kraj.data == 'POL':
                            obszar = FirmyObszarDzialania(
                                id_firmy=company.id_firmy,
                                id_kraj='POL',
                                id_wojewodztwa='N/A',
                                id_powiaty=0
                            )
                            db.session.add(obszar)
                elif obszar_type == 'wojewodztwa':
                    for woj_id in form.wojewodztwa.data:
                        obszar = FirmyObszarDzialania(
                            id_firmy=company.id_firmy,
                            id_kraj='N/A',
                            id_wojewodztwa=woj_id,
                            id_powiaty=0
                        )
                        db.session.add(obszar)
                elif obszar_type == 'powiaty':
                    for pow_id in form.powiaty.data:
                        powiat = Powiaty.query.get(pow_id)
                        obszar = FirmyObszarDzialania(
                            id_firmy=company.id_firmy,
                            id_kraj='N/A',
                            id_wojewodztwa=powiat.id_wojewodztwa,
                            id_powiaty=pow_id
                        )
                        db.session.add(obszar)

                # Add specialties
                for spec_id in form.specjalnosci.data:
                    spec = FirmySpecjalnosci(
                        id_firmy=company.id_firmy,
                        id_specjalnosci=spec_id
                    )
                    db.session.add(spec)

            db.session.commit()
            flash('Firma została dodana pomyślnie!', 'success')
            return redirect(url_for('main.company_details', company_id=company.id_firmy))
        else:
            if form.errors:
                flash(f'Błędy w formularzu: {form.errors}', 'danger')
                return render_template('company_form.html', form=form, title='Nowa firma')

    return render_template('company_form.html', form=form, title='Nowa firma')

@main.route('/company/<int:company_id>/edit', methods=['GET', 'POST'])
def edit_company(company_id):
    from app.forms import CompanyForm

    company = Firmy.query.get_or_404(company_id)
    form = CompanyForm(obj=company)

    if request.method == 'GET':
        form.nazwa_firmy.data = company.nazwa_firmy
        form.typ_firmy.data = company.id_firmy_typ
        form.strona_www.data = company.strona_www
        form.uwagi.data = company.uwagi

        adresy = Adresy.query.filter_by(id_firmy=company_id).all()
        while len(form.adresy) < len(adresy):
            form.adresy.append_entry()
        for i, adres in enumerate(adresy):
            form.adresy[i].typ_adresu.data = adres.id_adresy_typ
            form.adresy[i].kod.data = adres.kod
            form.adresy[i].miejscowosc.data = adres.miejscowosc
            form.adresy[i].ulica_miejscowosc.data = adres.ulica_miejscowosc

        emaile = Email.query.filter_by(id_firmy=company_id).all()
        while len(form.emaile) < len(emaile):
            form.emaile.append_entry()
            form.emaile[-1].typ_emaila.choices = form.email_type_choices
        for i, email in enumerate(emaile):
            form.emaile[i].typ_emaila.data = email.id_email_typ
            form.emaile[i].email.data = email.e_mail

        telefony = Telefon.query.filter_by(id_firmy=company_id).all()
        while len(form.telefony) < len(telefony):
            form.telefony.append_entry()
        for i, telefon in enumerate(telefony):
            form.telefony[i].typ_telefonu.data = telefon.id_telefon_typ
            form.telefony[i].telefon.data = telefon.telefon

        osoby = Osoby.query.filter_by(id_firmy=company_id).all()
        while len(form.osoby) < len(osoby):
            form.osoby.append_entry()
        for i, osoba in enumerate(osoby):
            form.osoby[i].imie.data = osoba.imie
            form.osoby[i].nazwisko.data = osoba.nazwisko
            form.osoby[i].stanowisko.data = osoba.stanowisko
            form.osoby[i].email.data = osoba.e_mail
            form.osoby[i].telefon.data = osoba.telefon

        oceny = Oceny.query.filter_by(id_firmy=company_id).all()
        while len(form.oceny) < len(oceny):
            form.oceny.append_entry()
        for i, ocena in enumerate(oceny):
            form.oceny[i].osoba_oceniajaca.data = ocena.osoba_oceniajaca
            form.oceny[i].budowa_dzial.data = ocena.budowa_dzial
            form.oceny[i].rok_wspolpracy.data = ocena.rok_wspolpracy
            form.oceny[i].ocena.data = ocena.ocena
            form.oceny[i].komentarz.data = ocena.komentarz

        obszary = FirmyObszarDzialania.query.filter_by(id_firmy=company_id).all()

        obszar_krajowy = next((o for o in obszary if o.id_kraj == 'POL'), None)
        if obszar_krajowy:
            form.obszar_dzialania.data = 'kraj'
            form.kraj.data = 'POL'
        else:
            has_powiaty = any(o.id_powiaty > 0 for o in obszary)
            if has_powiaty:
                form.obszar_dzialania.data = 'powiaty'
            else:
                has_wojewodztwa = any(o.id_wojewodztwa for o in obszary)
                if has_wojewodztwa:
                    form.obszar_dzialania.data = 'wojewodztwa'
                else:
                    form.obszar_dzialania.data = 'kraj'

            form.kraj.data = ''
            wojewodztwa_ids = list(set([o.id_wojewodztwa for o in obszary if o.id_wojewodztwa]))
            form.wojewodztwa.data = [w for w in wojewodztwa_ids if w]
            powiaty_ids = [o.id_powiaty for o in obszary if o.id_powiaty and o.id_powiaty > 0]
            form.powiaty.data = powiaty_ids

        specjalnosci = FirmySpecjalnosci.query.filter_by(id_firmy=company_id).all()
        form.specjalnosci.data = [s.id_specjalnosci for s in specjalnosci]

    elif request.method == 'POST':
        if form.validate_on_submit():
            company.nazwa_firmy = form.nazwa_firmy.data
            company.id_firmy_typ = form.typ_firmy.data
            company.strona_www = form.strona_www.data
            company.uwagi = form.uwagi.data

            with db.session.no_autoflush:
                Adresy.query.filter_by(id_firmy=company_id).delete()
                Email.query.filter_by(id_firmy=company_id).delete()
                Telefon.query.filter_by(id_firmy=company_id).delete()
                Osoby.query.filter_by(id_firmy=company_id).delete()
                Oceny.query.filter_by(id_firmy=company_id).delete()
                FirmyObszarDzialania.query.filter_by(id_firmy=company_id).delete()
                FirmySpecjalnosci.query.filter_by(id_firmy=company_id).delete()

                db.session.flush()

                for address_form in form.adresy:
                    if address_form.miejscowosc.data:
                        address = Adresy(
                            kod=address_form.kod.data,
                            miejscowosc=address_form.miejscowosc.data,
                            ulica_miejscowosc=address_form.ulica_miejscowosc.data,
                            id_adresy_typ=address_form.typ_adresu.data,
                            id_firmy=company_id
                        )
                        db.session.add(address)

            for email_form in form.emaile:
                if email_form.email.data:
                    email = Email(
                        e_mail=email_form.email.data,
                        id_email_typ=email_form.typ_emaila.data,
                        id_firmy=company_id
                    )
                    db.session.add(email)

            for phone_form in form.telefony:
                if phone_form.telefon.data:
                    phone = Telefon(
                        telefon=phone_form.telefon.data,
                        id_telefon_typ=phone_form.typ_telefonu.data,
                        id_firmy=company_id
                    )
                    db.session.add(phone)

            for person_form in form.osoby:
                if person_form.imie.data and person_form.nazwisko.data:
                    person = Osoby(
                        imie=person_form.imie.data,
                        nazwisko=person_form.nazwisko.data,
                        stanowisko=person_form.stanowisko.data,
                        e_mail=person_form.email.data,
                        telefon=person_form.telefon.data,
                        id_firmy=company_id
                    )
                    db.session.add(person)

            for rating_form in form.oceny:
                if rating_form.osoba_oceniajaca.data:
                    rating = Oceny(
                        osoba_oceniajaca=rating_form.osoba_oceniajaca.data,
                        budowa_dzial=rating_form.budowa_dzial.data,
                        rok_wspolpracy=rating_form.rok_wspolpracy.data,
                        ocena=rating_form.ocena.data,
                        komentarz=rating_form.komentarz.data,
                        id_firmy=company_id
                    )
                    db.session.add(rating)

            obszar_type = form.obszar_dzialania.data

            if obszar_type == 'kraj':
                    if form.kraj.data == 'POL':
                        obszar = FirmyObszarDzialania(
                            id_firmy=company.id_firmy,
                            id_kraj='POL',
                            id_wojewodztwa='N/A',
                            id_powiaty=0
                        )
                        db.session.add(obszar)
            elif obszar_type == 'wojewodztwa':
                for woj_id in form.wojewodztwa.data:
                    obszar = FirmyObszarDzialania(
                        id_firmy=company.id_firmy,
                        id_kraj='N/A',
                        id_wojewodztwa=woj_id,
                        id_powiaty=0
                    )
                    db.session.add(obszar)
            elif obszar_type == 'powiaty':
                for pow_id in form.powiaty.data:
                    powiat = Powiaty.query.get(pow_id)
                    obszar = FirmyObszarDzialania(
                        id_firmy=company.id_firmy,
                        id_kraj='N/A',
                        id_wojewodztwa=powiat.id_wojewodztwa,
                        id_powiaty=pow_id
                    )
                    db.session.add(obszar)

            for spec_id in form.specjalnosci.data:
                spec = FirmySpecjalnosci(
                    id_firmy=company_id,
                    id_specjalnosci=spec_id
                )
                db.session.add(spec)

            db.session.commit()
            flash('Firma została zaktualizowana pomyślnie!', 'success')
            return redirect(url_for('main.company_details', company_id=company_id))

        else:
            flash(f'Błędy w formularzu: {form.errors}', 'danger')

    return render_template('company_form.html', 
                          form=form, 
                          title='Edycja firmy',
                          company_id=company_id)

@main.route('/company/<int:company_id>/delete', methods=['POST'])
def delete_company(company_id):
    company = Firmy.query.get_or_404(company_id)
    try:
        Adresy.query.filter_by(id_firmy=company_id).delete()
        Email.query.filter_by(id_firmy=company_id).delete()
        Telefon.query.filter_by(id_firmy=company_id).delete()
        Osoby.query.filter_by(id_firmy=company_id).delete()
        Oceny.query.filter_by(id_firmy=company_id).delete()
        FirmyObszarDzialania.query.filter_by(id_firmy=company_id).delete()
        FirmySpecjalnosci.query.filter_by(id_firmy=company_id).delete()
        db.session.delete(company)
        db.session.commit()
        flash('Firma została usunięta pomyślnie!', 'success')
        return jsonify({'success': True, 'redirect': url_for('main.list_companies')})
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania firmy: {str(e)}', 'danger')
        return jsonify({'success': False, 'error': str(e)}), 500
