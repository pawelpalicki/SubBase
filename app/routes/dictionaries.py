from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import db
from app.models import FirmyTyp, Specjalnosci, AdresyTyp, EmailTyp, TelefonTyp, Category, WorkType
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from . import main

# --- API Endpoints ---

@main.route('/api/adres_typ', methods=['POST'])
@login_required
def add_adres_typ():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Brak wymaganych danych'}), 400

    try:
        # Sprawdzamy, czy typ już istnieje
        existing = AdresyTyp.query.filter_by(typ_adresu=data['name']).first()
        if existing:
            return jsonify({'error': 'Ten typ adresu już istnieje', 'id': existing.id_adresy_typ}), 400

        # Dodajemy nowy typ adresu
        new_typ = AdresyTyp(typ_adresu=data['name'])
        db.session.add(new_typ)
        db.session.commit()

        return jsonify({'id': new_typ.id_adresy_typ, 'name': new_typ.typ_adresu}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/email_typ', methods=['POST'])
@login_required
def add_email_typ():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Brak wymaganych danych'}), 400

    try:
        # Sprawdzamy, czy typ już istnieje
        existing = EmailTyp.query.filter_by(typ_emaila=data['name']).first()
        if existing:
            return jsonify({'error': 'Ten typ emaila już istnieje', 'id': existing.id_email_typ}), 400

        # Dodajemy nowy typ emaila
        new_typ = EmailTyp(typ_emaila=data['name'])
        db.session.add(new_typ)
        db.session.commit()

        return jsonify({'id': new_typ.id_email_typ, 'name': new_typ.typ_emaila}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/telefon_typ', methods=['POST'])
@login_required
def add_telefon_typ():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Brak wymaganych danych'}), 400

    try:
        # Sprawdzamy, czy typ już istnieje
        existing = TelefonTyp.query.filter_by(typ_telefonu=data['name']).first()
        if existing:
            return jsonify({'error': 'Ten typ telefonu już istnieje', 'id': existing.id_telefon_typ}), 400

        # Dodajemy nowy typ telefonu
        new_typ = TelefonTyp(typ_telefonu=data['name'])
        db.session.add(new_typ)
        db.session.commit()

        return jsonify({'id': new_typ.id_telefon_typ, 'name': new_typ.typ_telefonu}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/firma_typ', methods=['POST'])
@login_required
def add_firma_typ():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Brak wymaganych danych'}), 400

    try:
        # Sprawdzamy, czy typ już istnieje
        existing = FirmyTyp.query.filter_by(typ_firmy=data['name']).first()
        if existing:
            return jsonify({'error': 'Ten typ firmy już istnieje', 'id': existing.id_firmy_typ}), 400

        # Dodajemy nowy typ firmy
        new_typ = FirmyTyp(typ_firmy=data['name'])
        db.session.add(new_typ)
        db.session.commit()

        return jsonify({'id': new_typ.id_firmy_typ, 'name': new_typ.typ_firmy}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/specjalnosc', methods=['POST'])
@login_required
def add_specjalnosc():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Brak wymaganych danych'}), 400

    try:
        # Sprawdzamy, czy specjalność już istnieje
        existing = Specjalnosci.query.filter_by(specjalnosc=data['name']).first()
        if existing:
            return jsonify({'error': 'Ta specjalność już istnieje', 'id': existing.id_specjalnosci}), 400

        # Dodajemy nową specjalność
        new_spec = Specjalnosci(specjalnosc=data['name'])
        db.session.add(new_spec)
        db.session.commit()

        return jsonify({'id': new_spec.id_specjalnosci, 'name': new_spec.specjalnosc}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- CRUD Views for Dictionaries ---

# Specialties
@main.route('/specialties')
@login_required
def list_specialties():
    specialties = Specjalnosci.query.all()
    return render_template('specialties.html', items=specialties, title='Specjalności')

@main.route('/specialties/new', methods=['GET', 'POST'])
@login_required
def new_specialty():
    from app.forms import SpecialtyForm
    form = SpecialtyForm()
    if form.validate_on_submit():
        try:
            existing_spec = Specjalnosci.query.filter(func.lower(Specjalnosci.specjalnosc) == func.lower(form.name.data)).first()
            if existing_spec:
                flash('Specjalność o tej nazwie już istnieje.', 'warning')
            else:
                new_spec = Specjalnosci(specjalnosc=form.name.data)
                db.session.add(new_spec)
                db.session.commit()
                flash('Specjalność została dodana pomyślnie!', 'success')
                return redirect(url_for('main.list_specialties'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania specjalności: {e}', 'danger')
    return render_template('simple_form.html', form=form, title='Dodaj Specjalność', back_url=url_for('main.list_specialties'))

@main.route('/specialties/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_specialty(id):
    from app.forms import SpecialtyForm
    specialty = Specjalnosci.query.get_or_404(id)
    form = SpecialtyForm(obj=specialty)
    if request.method == 'GET':
        form.name.data = specialty.specjalnosc
        return render_template('simple_form.html', form=form, title='Edytuj Specjalność', back_url=url_for('main.list_specialties'))
    else:
        if form.validate_on_submit():
            try:
                existing_spec = Specjalnosci.query.filter(func.lower(Specjalnosci.specjalnosc) == func.lower(form.name.data), Specjalnosci.id_specjalnosci != id).first()
                if existing_spec:
                    flash('Specjalność o tej nazwie już istnieje.', 'warning')
                else:
                    specialty.specjalnosc = form.name.data
                    db.session.commit()
                    flash('Specjalność została zaktualizowana pomyślnie!', 'success')
                    return redirect(url_for('main.list_specialties'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'Wystąpił błąd podczas aktualizacji specjalności: {e}', 'danger')
        return render_template('simple_form.html', form=form, title='Edytuj Specjalność', back_url=url_for('main.list_specialties'))

@main.route('/specialties/<int:id>/delete', methods=['POST'])
@login_required
def delete_specialty(id):
    specialty = Specjalnosci.query.get_or_404(id)
    try:
        db.session.delete(specialty)
        db.session.commit()
        flash('Specjalność została usunięta pomyślnie!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania specjalności: {e}', 'danger')
    return redirect(url_for('main.list_specialties'))

# Address Types
@main.route('/address_types')
@login_required
def list_address_types():
    address_types = AdresyTyp.query.all()
    return render_template('address_types.html', items=address_types, title='Typy Adresów')

@main.route('/address_types/new', methods=['GET', 'POST'])
@login_required
def new_address_type():
    from app.forms import AddressTypeForm
    form = AddressTypeForm()
    if form.validate_on_submit():
        try:
            existing_type = AdresyTyp.query.filter(func.lower(AdresyTyp.typ_adresu) == func.lower(form.name.data)).first()
            if existing_type:
                flash('Typ adresu o tej nazwie już istnieje.', 'warning')
            else:
                new_type = AdresyTyp(typ_adresu=form.name.data)
                db.session.add(new_type)
                db.session.commit()
                flash('Typ adresu został dodany pomyślnie!', 'success')
                return redirect(url_for('main.list_address_types'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania typu adresu: {e}', 'danger')
    return render_template('simple_form.html', form=form, title='Dodaj Typ Adresu', back_url=url_for('main.list_address_types'))

@main.route('/address_types/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_address_type(id):
    from app.forms import AddressTypeForm
    address_type = AdresyTyp.query.get_or_404(id)
    form = AddressTypeForm(obj=address_type)
    if request.method == 'GET':
        form.name.data = address_type.typ_adresu
        return render_template('simple_form.html', form=form, title='Edytuj Typ Adresu', back_url=url_for('main.list_address_types'))
    else:
        if form.validate_on_submit():
            try:
                existing_type = AdresyTyp.query.filter(func.lower(AdresyTyp.typ_adresu) == func.lower(form.name.data), AdresyTyp.id_adresy_typ != id).first()
                if existing_type:
                    flash('Typ adresu o tej nazwie już istnieje.', 'warning')
                else:
                    address_type.typ_adresu = form.name.data
                    db.session.commit()
                    flash('Typ adresu został zaktualizowany pomyślnie!', 'success')
                    return redirect(url_for('main.list_address_types'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'Wystąpił błąd podczas aktualizacji typu adresu: {e}', 'danger')
        return render_template('simple_form.html', form=form, title='Edytuj Typ Adresu', back_url=url_for('main.list_address_types'))

@main.route('/address_types/<int:id>/delete', methods=['POST'])
@login_required
def delete_address_type(id):
    address_type = AdresyTyp.query.get_or_404(id)
    try:
        db.session.delete(address_type)
        db.session.commit()
        flash('Typ adresu został usunięty pomyślnie!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania typu adresu: {e}', 'danger')
    return redirect(url_for('main.list_address_types'))

# Email Types
@main.route('/email_types')
@login_required
def list_email_types():
    email_types = EmailTyp.query.all()
    return render_template('email_types.html', items=email_types, title='Typy E-maili')

@main.route('/email_types/new', methods=['GET', 'POST'])
@login_required
def new_email_type():
    from app.forms import EmailTypeForm
    form = EmailTypeForm()
    if form.validate_on_submit():
        try:
            existing_type = EmailTyp.query.filter(func.lower(EmailTyp.typ_emaila) == func.lower(form.name.data)).first()
            if existing_type:
                flash('Typ emaila o tej nazwie już istnieje.', 'warning')
            else:
                new_type = EmailTyp(typ_emaila=form.name.data)
                db.session.add(new_type)
                db.session.commit()
                flash('Typ emaila został dodany pomyślnie!', 'success')
                return redirect(url_for('main.list_email_types'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania typu emaila: {e}', 'danger')
    return render_template('simple_form.html', form=form, title='Dodaj Typ E-maila', back_url=url_for('main.list_email_types'))

@main.route('/email_types/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_email_type(id):
    from app.forms import EmailTypeForm
    email_type = EmailTyp.query.get_or_404(id)
    form = EmailTypeForm(obj=email_type)
    if request.method == 'GET':
        form.name.data = email_type.typ_emaila
        return render_template('simple_form.html', form=form, title='Edytuj Typ E-maila', back_url=url_for('main.list_email_types'))
    else:
        if form.validate_on_submit():
            try:
                existing_type = EmailTyp.query.filter(func.lower(EmailTyp.typ_emaila) == func.lower(form.name.data), EmailTyp.id_email_typ != id).first()
                if existing_type:
                    flash('Typ emaila o tej nazwie już istnieje.', 'warning')
                else:
                    email_type.typ_emaila = form.name.data
                    db.session.commit()
                    flash('Typ emaila został zaktualizowany pomyślnie!', 'success')
                    return redirect(url_for('main.list_email_types'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'Wystąpił błąd podczas aktualizacji typu emaila: {e}', 'danger')
        return render_template('simple_form.html', form=form, title='Edytuj Typ E-maila', back_url=url_for('main.list_email_types'))

@main.route('/email_types/<int:id>/delete', methods=['POST'])
@login_required
def delete_email_type(id):
    email_type = EmailTyp.query.get_or_404(id)
    try:
        db.session.delete(email_type)
        db.session.commit()
        flash('Typ emaila został usunięty pomyślnie!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania typu emaila: {e}', 'danger')
    return redirect(url_for('main.list_email_types'))

# Phone Types
@main.route('/phone_types')
@login_required
def list_phone_types():
    phone_types = TelefonTyp.query.all()
    return render_template('phone_types.html', items=phone_types, title='Typy Telefonów')

@main.route('/phone_types/new', methods=['GET', 'POST'])
@login_required
def new_phone_type():
    from app.forms import PhoneTypeForm
    form = PhoneTypeForm()
    if form.validate_on_submit():
        try:
            existing_type = TelefonTyp.query.filter(func.lower(TelefonTyp.typ_telefonu) == func.lower(form.name.data)).first()
            if existing_type:
                flash('Typ telefonu o tej nazwie już istnieje.', 'warning')
            else:
                new_type = TelefonTyp(typ_telefonu=form.name.data)
                db.session.add(new_type)
                db.session.commit()
                flash('Typ telefonu został dodany pomyślnie!', 'success')
                return redirect(url_for('main.list_phone_types'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania typu telefonu: {e}', 'danger')
    return render_template('simple_form.html', form=form, title='Dodaj Typ Telefonu', back_url=url_for('main.list_phone_types'))

@main.route('/phone_types/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_phone_type(id):
    from app.forms import PhoneTypeForm
    phone_type = TelefonTyp.query.get_or_404(id)
    form = PhoneTypeForm(obj=phone_type)
    if request.method == 'GET':
        form.name.data = phone_type.typ_telefonu
        return render_template('simple_form.html', form=form, title='Edytuj Typ Telefonu', back_url=url_for('main.list_phone_types'))
    else:
        if form.validate_on_submit():
            try:
                existing_type = TelefonTyp.query.filter(func.lower(TelefonTyp.typ_telefonu) == func.lower(form.name.data), TelefonTyp.id_telefon_typ != id).first()
                if existing_type:
                    flash('Typ telefonu o tej nazwie już istnieje.', 'warning')
                else:
                    phone_type.typ_telefonu = form.name.data
                    db.session.commit()
                    flash('Typ telefonu został zaktualizowany pomyślnie!', 'success')
                    return redirect(url_for('main.list_phone_types'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'Wystąpił błąd podczas aktualizacji typu telefonu: {e}', 'danger')
        return render_template('simple_form.html', form=form, title='Edytuj Typ Telefonu', back_url=url_for('main.list_phone_types'))

@main.route('/phone_types/<int:id>/delete', methods=['POST'])
@login_required
def delete_phone_type(id):
    phone_type = TelefonTyp.query.get_or_404(id)
    try:
        db.session.delete(phone_type)
        db.session.commit()
        flash('Typ telefonu został usunięty pomyślnie!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania typu telefonu: {e}', 'danger')
    return redirect(url_for('main.list_phone_types'))

# Company Types
@main.route('/company_types')
@login_required
def list_company_types():
    company_types = FirmyTyp.query.all()
    return render_template('company_types.html', items=company_types, title='Typy Firm')

@main.route('/company_types/new', methods=['GET', 'POST'])
@login_required
def new_company_type():
    from app.forms import CompanyTypeForm
    form = CompanyTypeForm()
    if form.validate_on_submit():
        try:
            existing_type = FirmyTyp.query.filter(func.lower(FirmyTyp.typ_firmy) == func.lower(form.name.data)).first()
            if existing_type:
                flash('Typ firmy o tej nazwie już istnieje.', 'warning')
            else:
                new_type = FirmyTyp(typ_firmy=form.name.data)
                db.session.add(new_type)
                db.session.commit()
                flash('Typ firmy został dodany pomyślnie!', 'success')
                return redirect(url_for('main.list_company_types'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania typu firmy: {e}', 'danger')
    return render_template('simple_form.html', form=form, title='Dodaj Typ Firmy', back_url=url_for('main.list_company_types'))

@main.route('/company_types/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_company_type(id):
    from app.forms import CompanyTypeForm
    company_type = FirmyTyp.query.get_or_404(id)
    form = CompanyTypeForm(obj=company_type)
    if request.method == 'GET':
        form.name.data = company_type.typ_firmy
        return render_template('simple_form.html', form=form, title='Edytuj Typ Firmy', back_url=url_for('main.list_company_types'))
    else:
        if form.validate_on_submit():
            try:
                existing_type = FirmyTyp.query.filter(func.lower(FirmyTyp.typ_firmy) == func.lower(form.name.data), FirmyTyp.id_firmy_typ != id).first()
                if existing_type:
                    flash('Typ firmy o tej nazwie już istnieje.', 'warning')
                else:
                    company_type.typ_firmy = form.name.data
                    db.session.commit()
                    flash('Typ firmy został zaktualizowany pomyślnie!', 'success')
                    return redirect(url_for('main.list_company_types'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'Wystąpił błąd podczas aktualizacji typu firmy: {e}', 'danger')
        return render_template('simple_form.html', form=form, title='Edytuj Typ Firmy', back_url=url_for('main.list_company_types'))

@main.route('/company_types/<int:id>/delete', methods=['POST'])
@login_required
def delete_company_type(id):
    company_type = FirmyTyp.query.get_or_404(id)
    try:
        db.session.delete(company_type)
        db.session.commit()
        flash('Typ firmy został usunięty pomyślnie!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania typu firmy: {e}', 'danger')
    return redirect(url_for('main.list_company_types'))

# --- Categories Routes ---

@main.route('/categories')
@login_required
def list_categories():
    categories = Category.query.order_by(Category.nazwa_kategorii).all()
    return render_template('categories.html', categories=categories, title='Kategorie Cen Jednostkowych')

@main.route('/categories/new', methods=['GET', 'POST'])
@login_required
def new_category():
    from app.forms import CategoryForm
    form = CategoryForm()
    if form.validate_on_submit():
        try:
            new_category = Category(nazwa_kategorii=form.name.data)
            db.session.add(new_category)
            db.session.commit()
            flash('Nowa kategoria została dodana.', 'success')
            return redirect(url_for('main.list_categories'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania kategorii: {e}', 'danger')
    return render_template('simple_form.html', form=form, title='Nowa Kategoria', back_url=url_for('main.list_categories'))

@main.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    from app.forms import CategoryForm
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.nazwa_kategorii = form.name.data
        db.session.commit()
        flash('Kategoria została zaktualizowana.', 'success')
        return redirect(url_for('main.list_categories'))
    if request.method == 'GET':
        form.name.data = category.nazwa_kategorii
    return render_template('simple_form.html', form=form, title='Edycja Kategorii', back_url=url_for('main.list_categories'))

@main.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    try:
        if category.unit_prices:
            flash('Nie można usunąć kategorii, która jest przypisana do pozycji cenowych.', 'danger')
            return redirect(url_for('main.list_categories'))
        WorkType.query.filter_by(id_kategorii=category_id).update({'id_kategorii': None})
        db.session.delete(category)
        db.session.commit()
        flash('Kategoria została usunięta.', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania kategorii: {e}', 'danger')
    return redirect(url_for('main.list_categories'))

# --- API Endpoints for Select2 (WorkTypes & Categories) ---

@main.route('/api/work_types', methods=['GET', 'POST'])
@login_required
def add_work_type():
    from app.forms import WorkTypeForm
    form = WorkTypeForm()
    if form.validate_on_submit():
        try:
            existing = WorkType.query.filter(func.lower(WorkType.name) == func.lower(form.name.data)).first()
            if existing:
                return jsonify({'success': False, 'errors': {'name': ['Ta nazwa roboty już istnieje.']}}), 422
            new_work_type = WorkType(
                name=form.name.data,
                id_kategorii=form.id_kategorii.data
            )
            db.session.add(new_work_type)
            db.session.commit()
            return jsonify({'success': True, 'id': new_work_type.id, 'name': new_work_type.name}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'success': False, 'errors': {'_form': [f'Błąd bazy danych: {str(e)}']}}), 500
    if request.method == 'POST':
        return jsonify({'success': False, 'errors': form.errors}), 422

    work_type_name = request.args.get('work_type_name')
    category_id = request.args.get('category_id')
    if work_type_name:
        form.name.data = work_type_name
    if category_id:
        form.id_kategorii.data = int(category_id)
    
    if request.args.get('_partial') == 'true':
        return render_template('_work_type_form_partial.html', form=form)
    else:
        return render_template('work_type_form.html', form=form, title='Nowy Rodzaj Roboty', back_url=url_for('main.list_work_types'))

@main.route('/api/categories', methods=['GET', 'POST'])
@login_required
def add_category():
    from app.forms import CategoryForm
    form = CategoryForm()
    if form.validate_on_submit():
        try:
            existing = Category.query.filter(func.lower(Category.nazwa_kategorii) == func.lower(form.name.data)).first()
            if existing:
                return jsonify({'success': False, 'errors': {'name': ['Ta kategoria już istnieje.']}}), 422
            new_category = Category(nazwa_kategorii=form.name.data)
            db.session.add(new_category)
            db.session.commit()
            return jsonify({'success': True, 'id': new_category.id, 'name': new_category.nazwa_kategorii}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'success': False, 'errors': {'_form': [f'Błąd bazy danych: {str(e)}']}}), 500
    if request.method == 'POST':
        return jsonify({'success': False, 'errors': form.errors}), 422
    
    if request.args.get('_partial') == 'true':
        return render_template('_category_form_partial.html', form=form)
    else:
        return render_template('simple_category_form.html', form=form, title='Nowa Kategoria', back_url=url_for('main.list_categories'))

@main.route('/api/categories/form', methods=['GET', 'POST'])
@login_required
def get_category_form():
    from app.forms import CategoryForm
    form = CategoryForm()
    if form.validate_on_submit():
        try:
            existing = Category.query.filter(func.lower(Category.nazwa_kategorii) == func.lower(form.name.data)).first()
            if existing:
                form.name.errors.append('Ta kategoria już istnieje.')
                return render_template('category_form_modal.html', form=form), 400
            new_category = Category(nazwa_kategorii=form.name.data)
            db.session.add(new_category)
            db.session.commit()
            return jsonify({'success': True, 'id': new_category.id, 'name': new_category.nazwa_kategorii}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            form.name.errors.append(f'Błąd bazy danych: {str(e)}')
            return render_template('category_form_modal.html', form=form), 500
    return render_template('category_form_modal.html', form=form)

@main.route('/api/work_types_list')
@login_required
def api_work_types_list():
    query = request.args.get('q', '')
    work_types = WorkType.query.filter(WorkType.name.ilike(f'%{query}%')).order_by(WorkType.name).limit(20).all()
    results = [{'id': wt.id, 'text': wt.name} for wt in work_types]
    return jsonify(results)

@main.route('/api/categories_list')
@login_required
def api_categories_list():
    query = request.args.get('q', '')
    categories = Category.query.filter(Category.name.ilike(f'%{query}%')).order_by(Category.name).limit(20).all()
    results = [{'id': cat.id, 'text': cat.name} for cat in categories]
    return jsonify(results)

@main.route('/api/work_type_category/<int:work_type_id>')
@login_required
def get_work_type_category(work_type_id):
    work_type = WorkType.query.get(work_type_id)
    if work_type and work_type.category:
        return jsonify({'id': work_type.category.id, 'name': work_type.category.nazwa_kategorii})
    return jsonify({'id': 0, 'name': 'Brak kategorii'})

# --- Work Types Routes ---

@main.route('/work_types')
@login_required
def list_work_types():
    work_types = WorkType.query.order_by(WorkType.name).all()
    return render_template('work_types.html', items=work_types, title='Rodzaje Robót')

@main.route('/work_types/new', methods=['GET', 'POST'])
@login_required
def new_work_type():
    from app.forms import WorkTypeForm
    form = WorkTypeForm()
    if form.validate_on_submit():
        try:
            new_work_type = WorkType(
                name=form.name.data,
                id_kategorii=form.id_kategorii.data
            )
            db.session.add(new_work_type)
            db.session.commit()
            flash('Rodzaj roboty został dodany pomyślnie!', 'success')
            return redirect(url_for('main.list_work_types'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania rodzaju roboty: {e}', 'danger')
    return render_template('work_type_form.html', form=form, title='Nowy Rodzaj Roboty', back_url=url_for('main.list_work_types'))

@main.route('/work_types/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_work_type(id):
    from app.forms import WorkTypeForm
    work_type = WorkType.query.get_or_404(id)
    form = WorkTypeForm(obj=work_type)
    if form.validate_on_submit():
        try:
            work_type.name = form.name.data
            work_type.id_kategorii = form.id_kategorii.data
            db.session.commit()
            flash('Rodzaj roboty został zaktualizowany pomyślnie!', 'success')
            return redirect(url_for('main.list_work_types'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas aktualizacji rodzaju roboty: {e}', 'danger')
    return render_template('work_type_form.html', form=form, title='Edytuj Rodzaj Roboty', back_url=url_for('main.list_work_types'))

@main.route('/work_types/<int:id>/delete', methods=['POST'])
@login_required
def delete_work_type(id):
    work_type = WorkType.query.get_or_404(id)
    if work_type.unit_prices.first():
        flash('Nie można usunąć rodzaju roboty, który jest przypisany do pozycji cenowych.', 'danger')
        return redirect(url_for('main.list_work_types'))
    try:
        db.session.delete(work_type)
        db.session.commit()
        flash('Rodzaj roboty został usunięty pomyślnie!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania rodzaju roboty: {e}', 'danger')
    return redirect (url_for('main.list_work_types'))
