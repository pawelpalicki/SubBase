from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, jsonify, send_file
from flask_login import login_required
from app import db
from app.models import Tender, Project, UnitPrice, Category, WorkType, Firmy
from sqlalchemy import func
from app.forms import TenderForm, UnitPriceForm
from app.storage_service import get_storage_service # <-- Główny import serwisu
import os
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import pdfplumber
import xlrd
import openpyxl
import io
import traceback
from sqlalchemy.orm import joinedload # Dodany import

tenders_bp = Blueprint('tenders', __name__, template_folder='templates', url_prefix='/tenders')


@tenders_bp.route('/')
@login_required
def list_tenders():
    query = Tender.query
    form = TenderForm()

    # Filtrowanie
    id_firmy = request.args.get('id_firmy', type=int)
    id_projektu = request.args.get('id_projektu', type=int)

    if id_firmy:
        query = query.filter(Tender.id_firmy == id_firmy)
    if id_projektu:
        query = query.filter(Tender.id_projektu == id_projektu)

    tenders = query.order_by(Tender.data_otrzymania.desc()).all()
    projects = Project.query.order_by(Project.nazwa_projektu).all()
    
    return render_template('tenders_list.html', tenders=tenders, projects=projects, form=form, title='Oferty')

@tenders_bp.route('/<int:tender_id>')
@login_required
def tender_details(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    return render_template('tender_details.html', tender=tender, title=f"Szczegóły oferty: {tender.nazwa_oferty}")

@tenders_bp.route('/download/<int:tender_id>')
@login_required
def download_file(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    if not tender.storage_path:
        flash('Do tej oferty nie ma przypisanego pliku.', 'warning')
        return redirect(url_for('tenders.tender_details', tender_id=tender.id))
        
    try:
        storage_service = get_storage_service()
        file_stream = storage_service.download(tender.storage_path)
        return send_file(file_stream, download_name=tender.original_filename, mimetype=tender.file_type, as_attachment=True)
    except FileNotFoundError:
        flash(f'Plik nie został znaleziony w lokalizacji: {tender.storage_path}', 'danger')
        return redirect(url_for('tenders.tender_details', tender_id=tender.id))
    except Exception as e:
        current_app.logger.error(f"Błąd pobierania pliku (tender_id: {tender_id}): {e}")
        flash(f'Wystąpił błąd podczas pobierania pliku.', 'danger')
        return redirect(url_for('tenders.tender_details', tender_id=tender.id))


@tenders_bp.route('/display/<int:tender_id>')
@login_required
def display_file(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    if not tender.storage_path:
        flash('Do tej oferty nie ma przypisanego pliku.', 'warning')
        return redirect(url_for('tenders.tender_details', tender_id=tender.id))

    try:
        storage_service = get_storage_service()
        file_stream = storage_service.download(tender.storage_path)
        return send_file(file_stream, mimetype=tender.file_type)
    except FileNotFoundError:
        flash(f'Plik nie został znaleziony w lokalizacji: {tender.storage_path}', 'danger')
        return redirect(url_for('tenders.tender_details', tender_id=tender.id))
    except Exception as e:
        current_app.logger.error(f"Błąd wyświetlania pliku (tender_id: {tender_id}): {e}")
        flash(f'Wystąpił błąd podczas wyświetlania pliku.', 'danger')
        return redirect(url_for('tenders.tender_details', tender_id=tender.id))


@tenders_bp.route('/<int:tender_id>/extract_data', methods=['GET', 'POST'])
@login_required
def extract_data(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    extracted_text = ""
    table_data = []
    unit_price_form = UnitPriceForm()
    unit_price_form.id_oferty.data = tender.id

    if unit_price_form.validate_on_submit():
        try:
            work_type_id = unit_price_form.id_work_type.data
            work_type = WorkType.query.get(work_type_id)
            category_id = work_type.id_kategorii if work_type else None
            new_unit_price = UnitPrice(
                id_work_type=work_type_id,
                nazwa_roboty=work_type.name if work_type else None,
                jednostka_miary=unit_price_form.jednostka_miary.data,
                cena_jednostkowa=float(unit_price_form.cena_jednostkowa.data.replace(',', '.')),
                id_oferty=tender.id,
                id_kategorii=category_id,
                uwagi=unit_price_form.uwagi.data
            )
            db.session.add(new_unit_price)
            db.session.commit()
            flash('Pozycja cenowa została dodana pomyślnie!', 'success')
            return redirect(url_for('tenders.extract_data', tender_id=tender.id, from_submit=True))
        except Exception as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania pozycji cenowej: {e}', 'danger')

    if request.method == 'GET' and not request.args.get('from_submit'):
        file_content = None
        if not tender.storage_path:
            flash("Brak pliku do przetworzenia.", "warning")
        else:
            try:
                storage_service = get_storage_service()
                file_stream = storage_service.download(tender.storage_path)
                file_content = io.BytesIO(file_stream.read())
            except Exception as e:
                flash(f"Nie udało się wczytać pliku: {e}", "danger")

        if file_content:
            file_content.seek(0)
            filename_lower = tender.original_filename.lower()
            is_image_file = False
            display_original_pdf = False

            try:
                if filename_lower.endswith('.pdf'):
                    pdf_extracted_successfully = False
                    try:
                        with pdfplumber.open(file_content) as pdf:
                            has_tables = False
                            for page in pdf.pages:
                                tables = page.extract_tables()
                                if tables:
                                    has_tables = True
                                    for table in tables:
                                        table_data.extend(table)
                            
                            if has_tables:
                                pdf_extracted_successfully = True
                            else:
                                extracted_text = "".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                                if extracted_text.strip():
                                    pdf_extracted_successfully = True
                    except Exception as pdf_error:
                        file_content.seek(0)
                        with fitz.open(stream=file_content, filetype="pdf") as doc:
                            for page in doc:
                                extracted_text += page.get_text("text", sort=True)
                            if extracted_text.strip():
                                pdf_extracted_successfully = True
                    
                    if not pdf_extracted_successfully:
                        display_original_pdf = True

                elif filename_lower.endswith('.xlsx'):
                    workbook = openpyxl.load_workbook(file_content, data_only=True)
                    for sheet in workbook.worksheets:
                        merged_ranges = list(sheet.merged_cells.ranges)
                        for merged_range in merged_ranges:
                            sheet.unmerge_cells(str(merged_range))

                        for row in sheet.iter_rows():
                            row_data = [str(cell.value) if cell.value is not None else "" for cell in row]
                            if any(row_data):
                                table_data.append(row_data)

                elif filename_lower.endswith('.xls'):
                    workbook = xlrd.open_workbook(file_contents=file_content.read())
                    for sheet in workbook.sheets():
                        for row_idx in range(sheet.nrows):
                            row_data = []
                            for col_idx in range(sheet.ncols):
                                cell_value = sheet.cell_value(row_idx, col_idx)
                                for rlo, rhi, clo, chi in sheet.merged_cells:
                                    if rlo <= row_idx < rhi and clo <= col_idx < chi:
                                        cell_value = sheet.cell_value(rlo, clo)
                                        break
                                row_data.append(str(cell_value) if cell_value is not None else "")
                            if any(row_data):
                                table_data.append(row_data)
                
                elif filename_lower.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                    is_image_file = True
                else:
                    flash(f'Nieobsługiwany typ pliku do ekstrakcji danych: "{tender.original_filename}" (typ MIME: {tender.file_type})', 'warning')

            except Exception as e:
                traceback.print_exc()
                flash(f'Wystąpił błąd podczas ekstrakcji danych: {e}', 'danger')
    
    return render_template('extract_helper.html', tender=tender, extracted_text=extracted_text, table_data=table_data, unit_price_form=unit_price_form, categories=Category.query.order_by(Category.nazwa_kategorii).all(), unit_prices=tender.unit_prices.all(), title="Ekstrakcja danych z oferty", is_image_file=is_image_file if 'is_image_file' in locals() else False, display_original_pdf=display_original_pdf if 'display_original_pdf' in locals() else False)

@tenders_bp.route('/<int:tender_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tender(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    form = TenderForm(obj=tender)
    
    if request.method == 'GET':
        form.delete_existing_file.data = False

    if form.validate_on_submit():
        storage_service = get_storage_service()
        
        # Obsługa usuwania istniejącego pliku
        if form.delete_existing_file.data and not form.plik_oferty.data:
            if tender.storage_path:
                try:
                    storage_service.delete(tender.storage_path)
                    tender.original_filename = None
                    tender.storage_path = None
                    tender.file_type = None
                    flash('Istniejący plik został usunięty.', 'info')
                except Exception as e:
                    flash(f"Błąd podczas usuwania pliku: {e}", "danger")

        # Obsługa nowego pliku
        if form.plik_oferty.data:
            plik = form.plik_oferty.data
            filename = secure_filename(plik.filename)
            
            # Usuń stary plik przed wgraniem nowego
            if tender.storage_path:
                try:
                    storage_service.delete(tender.storage_path)
                except Exception as e:
                    flash(f"Nie udało się usunąć starego pliku, ale kontynuowano wgrywanie nowego. Błąd: {e}", "warning")

            try:
                tender.storage_path = storage_service.upload(plik.stream, filename, plik.mimetype)
                tender.original_filename = filename
                tender.file_type = plik.mimetype
            except Exception as e:
                flash(f"Błąd podczas wgrywania nowego pliku: {e}", "danger")
                return redirect(url_for('tenders.edit_tender', tender_id=tender.id))

        tender.nazwa_oferty = form.nazwa_oferty.data
        tender.data_otrzymania = form.data_otrzymania.data
        tender.status = form.status.data
        tender.id_firmy = form.id_firmy.data
        tender.id_projektu = form.id_projektu.data if form.id_projektu.data else None
        
        db.session.commit()
        flash('Oferta została zaktualizowana.', 'success')
        return redirect(url_for('tenders.tender_details', tender_id=tender.id))
    
    return render_template('tender_form.html', form=form, tender=tender, title=f"Edycja oferty: {tender.nazwa_oferty}")


@tenders_bp.route('/<int:tender_id>/delete', methods=['POST'])
@login_required
def delete_tender(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    
    if tender.storage_path:
        try:
            storage_service = get_storage_service()
            storage_service.delete(tender.storage_path)
        except Exception as e:
            flash(f"Nie udało się usunąć pliku powiązanego z ofertą, ale oferta zostanie usunięta. Błąd: {e}", "warning")

    db.session.delete(tender)
    db.session.commit()
    flash('Oferta została usunięta.', 'success')
    return redirect(url_for('tenders.list_tenders'))

@tenders_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_tender():
    form = TenderForm()
    if form.validate_on_submit():
        if form.plik_oferty.data:
            plik = form.plik_oferty.data
            filename = secure_filename(plik.filename)

            try:
                storage_service = get_storage_service()
                storage_path = storage_service.upload(plik.stream, filename, plik.mimetype)

                nowa_oferta = Tender(
                    nazwa_oferty=form.nazwa_oferty.data,
                    data_otrzymania=form.data_otrzymania.data,
                    status=form.status.data,
                    id_firmy=form.id_firmy.data,
                    id_projektu=form.id_projektu.data if form.id_projektu.data else None,
                    original_filename=filename,
                    storage_path=storage_path, 
                    file_type=plik.mimetype
                )
                
                db.session.add(nowa_oferta)
                db.session.commit()

                flash('Nowa oferta została dodana pomyślnie!', 'success')
                return redirect(url_for('tenders.list_tenders'))

            except Exception as e:
                flash(f"Wystąpił błąd podczas przesyłania pliku: {e}", "danger")

        else:
            flash('Proszę załączyć plik oferty.', 'danger')
            
    return render_template('tender_form.html', form=form, title='Nowa Oferta')

@tenders_bp.route('/unit_prices')
@login_required
def list_all_unit_prices():
    PER_PAGE = 15 # Liczba elementów na stronę

    nazwa_roboty_filter = request.args.get('nazwa_roboty', type=int)
    kategoria_filter = request.args.get('kategoria', type=int)
    id_oferty_filter = request.args.get('id_oferty', type=int)
    id_firmy_filter = request.args.get('id_firmy', type=int)
    id_projektu_filter = request.args.get('id_projektu', type=int)
    page = request.args.get('page', 1, type=int) # Pobierz numer strony

    query = UnitPrice.query.join(WorkType).join(Tender).join(Firmy)

    if nazwa_roboty_filter:
        query = query.filter(UnitPrice.id_work_type == nazwa_roboty_filter)
    if kategoria_filter:
        query = query.filter(UnitPrice.id_kategorii == kategoria_filter)
    if id_oferty_filter:
        query = query.filter(UnitPrice.id_oferty == id_oferty_filter)
    if id_firmy_filter:
        query = query.filter(Tender.id_firmy == id_firmy_filter)
    if id_projektu_filter:
        query = query.filter(Tender.id_projektu == id_projektu_filter)

    # Paginacja
    pagination = query.order_by(UnitPrice.id.desc()).paginate(page=page, per_page=PER_PAGE, error_out=False)
    unit_prices = pagination.items # Elementy dla bieżącej strony

    work_types = WorkType.query.order_by(WorkType.name).all()
    categories = Category.query.order_by(Category.nazwa_kategorii).all()
    
    # Zoptymalizowane zapytanie do pobierania ofert do filtra
    all_tenders_for_filter = Tender.query.options(
        joinedload(Tender.firma),
        joinedload(Tender.project)
    ).order_by(Tender.data_otrzymania.desc()).all()

    # Formatowanie ofert dla listy rozwijanej filtra
    formatted_tenders_for_filter = []
    for t in all_tenders_for_filter:
        company_name = t.firma.nazwa_firmy if t.firma else "Brak firmy"
        if len(company_name) > 10:
            company_name = company_name[:10] + "..."

        project_info = "Brak projektu"
        if t.project:
            project_info = t.project.skrot if t.project.skrot else t.project.nazwa_projektu

        label = f"{t.nazwa_oferty} ({t.status}) - {company_name} ({project_info})"
        formatted_tenders_for_filter.append((t.id, label))

    firmy = Firmy.query.order_by(Firmy.nazwa_firmy).all()
    projects = Project.query.order_by(Project.nazwa_projektu).all()

    return render_template(
        'unit_prices_list.html',
        unit_prices=unit_prices,
        work_types=work_types,
        categories=categories,
        tenders=formatted_tenders_for_filter, # Przekazujemy sformatowane oferty
        firmy=firmy,
        projects=projects,
        selected_nazwa_roboty=nazwa_roboty_filter,
        selected_kategoria=kategoria_filter,
        selected_id_oferty=id_oferty_filter,
        selected_id_firmy=id_firmy_filter,
        selected_id_projektu=id_projektu_filter,
        pagination=pagination, # Przekazujemy obiekt paginacji
        title='Wszystkie pozycje cenowe'
    )

@tenders_bp.route('/unit_prices/analysis')
@login_required
def unit_prices_analysis():
    DEFAULT_TENDER_LIMIT = 10
    MAX_TENDER_LIMIT = 20

    category_filter = request.args.get('category', type=int)
    tender_ids_filter = request.args.getlist('tenders', type=int)

    work_types_query = WorkType.query.order_by(WorkType.name)
    if category_filter:
        work_types_query = work_types_query.filter(WorkType.id_kategorii == category_filter)
    all_work_types = work_types_query.all()

    tenders_truncated = False
    
    # Zapytanie bazowe dla ofert, zawsze sortowane od najnowszych
    base_tenders_query = Tender.query.options(
        joinedload(Tender.firma),
        joinedload(Tender.project)
    ).order_by(Tender.data_otrzymania.desc())

    if tender_ids_filter:
        # Jeśli filtry są podane, filtrujemy i ograniczamy do MAX_TENDER_LIMIT
        all_tenders = base_tenders_query.filter(Tender.id.in_(tender_ids_filter)).all()
        if len(all_tenders) > MAX_TENDER_LIMIT:
            all_tenders = all_tenders[:MAX_TENDER_LIMIT]
            tenders_truncated = True
            flash(f'Wybrano więcej niż {MAX_TENDER_LIMIT} ofert. Wyświetlono tylko {MAX_TENDER_LIMIT} najnowszych z wybranych.', 'info')
    else:
        # Jeśli brak filtrów, domyślnie 10 najnowszych
        all_tenders = base_tenders_query.limit(DEFAULT_TENDER_LIMIT).all()
        flash(f'Domyślnie wyświetlono {DEFAULT_TENDER_LIMIT} najnowszych ofert. Użyj filtrów, aby wybrać inne.', 'info')

    # Formatowanie nagłówków dla tabeli analizy
    formatted_tender_headers = {}
    # Określ próg, od którego nazwy firm będą skracane
    # Możesz dostosować tę wartość w zależności od preferencji
    SHORTEN_COMPANY_NAME_THRESHOLD = 5 

    for tender in all_tenders:
        company_name = tender.firma.nazwa_firmy if tender.firma else "Brak firmy"
        
        # Skracaj nazwę firmy tylko jeśli jest wiele kolumn
        if len(all_tenders) > SHORTEN_COMPANY_NAME_THRESHOLD and len(company_name) > 10:
            company_name = company_name[:10] + "..."

        project_info = "Brak projektu"
        if tender.project:
            project_info = tender.project.skrot if tender.project.skrot else tender.project.nazwa_projektu

        header_label = f"{company_name} ({project_info})"
        formatted_tender_headers[tender.id] = header_label

    unit_prices_query = UnitPrice.query.join(WorkType).join(Tender)
    if category_filter:
        unit_prices_query = unit_prices_query.filter(UnitPrice.id_kategorii == category_filter)
    # Filtruj ceny jednostkowe tylko dla ofert, które faktycznie zostaną wyświetlone
    if all_tenders: # Sprawdź, czy all_tenders nie jest puste
        unit_prices_query = unit_prices_query.filter(UnitPrice.id_oferty.in_([t.id for t in all_tenders]))
    else: # Jeśli nie ma ofert do wyświetlenia, nie pobieraj cen jednostkowych
        unit_prices_query = unit_prices_query.filter(False) # Zwróć pusty wynik

    all_unit_prices = unit_prices_query.all()

    prices_table = {}
    for up in all_unit_prices:
        if up.id_work_type not in prices_table:
            prices_table[up.id_work_type] = {}
        if up.id_oferty not in prices_table[up.id_work_type]:
            prices_table[up.id_work_type][up.id_oferty] = []

        prices_table[up.id_work_type][up.id_oferty].append({
            'cena': up.cena_jednostkowa,
            'uwagi': up.uwagi or ""
        })

    categories = Category.query.order_by(Category.nazwa_kategorii).all()
    # all_available_tenders do filtra ofert - to jest pełna lista, nie obcinamy jej
    all_available_tenders = Tender.query.order_by(Tender.nazwa_oferty).all()

    return render_template(
        'unit_prices_analysis.html',
        all_work_types=all_work_types,
        all_tenders=all_tenders, # Nadal przekazujemy all_tenders, ale już obcięte/domyślne
        prices_table=prices_table,
        categories=categories,
        all_available_tenders=all_available_tenders,
        selected_category=category_filter,
        selected_tenders=tender_ids_filter,
        formatted_tender_headers=formatted_tender_headers,
        tenders_truncated=tenders_truncated, # Nowa flaga
        title='Analiza cen jednostkowych'
    )

@tenders_bp.route('/unit_prices/analysis/time_series/<int:work_type_id>')
@login_required
def unit_prices_time_series_data(work_type_id):
    time_series_data = db.session.query(
        func.to_char(Tender.data_otrzymania, 'YYYY-MM'),
        func.avg(UnitPrice.cena_jednostkowa)
    ).join(Tender).filter(UnitPrice.id_work_type == work_type_id).group_by(func.to_char(Tender.data_otrzymania, 'YYYY-MM')).order_by(func.to_char(Tender.data_otrzymania, 'YYYY-MM')).all()

    labels = [row[0] for row in time_series_data]
    data = [float(row[1]) for row in time_series_data]

    return jsonify({'labels': labels, 'data': data})

@tenders_bp.route('/unit_prices/analysis/by_contractor/<int:work_type_id>')
@login_required
def unit_prices_by_contractor_data(work_type_id):
    contractor_data = db.session.query(
        Firmy.nazwa_firmy,
        func.avg(UnitPrice.cena_jednostkowa)
    ).select_from(UnitPrice).join(Tender).join(Firmy).filter(UnitPrice.id_work_type == work_type_id).group_by(Firmy.nazwa_firmy).order_by(Firmy.nazwa_firmy).all()

    labels = [row[0] for row in contractor_data]
    data = [float(row[1]) for row in contractor_data]

    return jsonify({'labels': labels, 'data': data})

@tenders_bp.route('/unit_prices/new_global', methods=['GET', 'POST'])
@login_required
def new_global_unit_price():
    form = UnitPriceForm()
    if form.validate_on_submit():
        try:
            work_type_id = form.id_work_type.data
            work_type = WorkType.query.get(work_type_id)
            category_id = work_type.id_kategorii if work_type else None
            new_unit_price = UnitPrice(
                id_work_type=work_type_id,
                nazwa_roboty=work_type.name if work_type else None,
                jednostka_miary=form.jednostka_miary.data,
                cena_jednostkowa=form.cena_jednostkowa.data,
                id_oferty=form.id_oferty.data,
                id_kategorii=category_id,
                uwagi=form.uwagi.data
            )
            db.session.add(new_unit_price)
            db.session.commit()
            flash('Pozycja cenowa została dodana pomyślnie!', 'success')
            return redirect(url_for('tenders.list_all_unit_prices'))
        except Exception as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania pozycji cenowej: {e}', 'danger')

    return render_template('unit_price_form.html', form=form, title='Dodaj nową pozycję cenową', show_tender_select=True, category_field_always_disabled_unless_auto_filled=True)

@tenders_bp.route('/unit_price/<int:price_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_unit_price(price_id):
    price = UnitPrice.query.get_or_404(price_id)
    form = UnitPriceForm(obj=price)
    if form.validate_on_submit():
        price.id_work_type = form.id_work_type.data
        work_type = WorkType.query.get(price.id_work_type)
        price.nazwa_roboty = work_type.name if work_type else None
        price.jednostka_miary = form.jednostka_miary.data
        price.cena_jednostkowa = form.cena_jednostkowa.data
        price.id_kategorii = work_type.id_kategorii if work_type else None
        price.uwagi = form.uwagi.data
        db.session.commit()
        flash('Pozycja cenowa została zaktualizowana.', 'success')
        return redirect(url_for('tenders.tender_details', tender_id=price.id_oferty))

    return render_template('unit_price_form.html', form=form, title='Edycja pozycji cenowej', tender_id=price.id_oferty, category_field_always_disabled_unless_auto_filled=True)

@tenders_bp.route('/unit_price/<int:price_id>/delete', methods=['POST'])
@login_required
def delete_unit_price(price_id):
    price = UnitPrice.query.get_or_404(price_id)
    tender_id = price.id_oferty
    db.session.delete(price)
    db.session.commit()
    flash('Pozycja cenowa została usunięta.', 'success')
    return redirect(url_for('tenders.tender_details', tender_id=tender_id))