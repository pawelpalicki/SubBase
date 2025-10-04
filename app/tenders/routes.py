from datetime import datetime
from statistics import median
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, jsonify, send_file, session
from flask_login import login_required, current_user
from app import db
from app.models import Tender, Project, UnitPrice, Category, WorkType, Firmy
from sqlalchemy import func, or_
from app.forms import TenderForm, UnitPriceForm
from app.storage_service import get_storage_service
import os
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import pdfplumber
import xlrd
import openpyxl
import io
import traceback
from sqlalchemy.orm import joinedload
import pandas as pd
import numpy as np
from google.cloud import vision

tenders_bp = Blueprint('tenders', __name__, template_folder='templates', url_prefix='/tenders')

def extract_and_save_text(tender):
    if not tender.storage_path:
        return

    try:
        storage_service = get_storage_service()
        file_stream = storage_service.download(tender.storage_path)
        file_content = io.BytesIO(file_stream.read())

        extracted_text = ""
        table_data = []

        filename_lower = tender.original_filename.lower()

        if filename_lower.endswith('.pdf'):
            text_found = False
            try:
                with pdfplumber.open(file_content) as pdf:
                    text = "".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                    if text.strip():
                        extracted_text += text
                        text_found = True
                    
                    for page in pdf.pages:
                        tables = page.extract_tables()
                        if tables:
                            for table in tables:
                                table_data.extend(table)
            except Exception as e:
                current_app.logger.error(f"Error with pdfplumber for tender {tender.id}: {e}")

            if not text_found and not table_data:
                try:
                    file_content.seek(0)
                    with fitz.open(stream=file_content, filetype="pdf") as doc:
                        text = "".join([page.get_text("text", sort=True) for page in doc])
                        if text.strip():
                            extracted_text += text
                            text_found = True
                except Exception as e:
                    current_app.logger.error(f"Error with fitz for tender {tender.id}: {e}")

            if not text_found and not table_data:
                try:
                    client = vision.ImageAnnotatorClient()
                    file_content.seek(0)
                    content = file_content.read()
                    image = vision.Image(content=content)
                    response = client.document_text_detection(image=image)
                    if response.full_text_annotation:
                        extracted_text += response.full_text_annotation.text
                except Exception as e:
                    current_app.logger.error(f"Error with Google Vision API for tender {tender.id}: {e}")
                    flash(f'Nie udało się przetworzyć skanu za pomocą OCR: {e}', 'warning')

        elif filename_lower.endswith('.xlsx'):
            workbook = openpyxl.load_workbook(file_content, data_only=True)
            for sheet in workbook.worksheets:
                for row in sheet.iter_rows():
                    row_data = [str(cell.value) if cell.value is not None else "" for cell in row]
                    if any(row_data):
                        table_data.append(row_data)

        elif filename_lower.endswith('.xls'):
            workbook = xlrd.open_workbook(file_contents=file_content.read())
            for sheet in workbook.sheets():
                for row_idx in range(sheet.nrows):
                    table_data.append([sheet.cell_value(row_idx, col_idx) for col_idx in range(sheet.ncols)])

        full_text = extracted_text
        if table_data:
            full_text += "\n\n" + "\n".join(["\t".join(map(str, row)) for row in table_data])

        tender.extracted_content = full_text.strip()
        db.session.commit()
        flash('Treść oferty została wyekstrahowana i zapisana.', 'info')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to extract and save text for tender {tender.id}: {e}")
        flash('Wystąpił błąd podczas ekstrakcji i zapisywania treści oferty.', 'danger')

@tenders_bp.route('/')
@login_required
def list_tenders():
    query = Tender.query
    form = TenderForm()
    search_query = request.args.get('q')

    if search_query:
        query = query.filter(Tender.extracted_content.ilike(f'%{search_query}%'))

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
        current_app.logger.error(f"Błąd pobierania pliku (tender_id: {tender.id}): {e}")
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
        current_app.logger.error(f"Błąd wyświetlania pliku (tender_id: {tender.id}): {e}")
        flash(f'Wystąpił błąd podczas wyświetlania pliku.', 'danger')
        return redirect(url_for('tenders.tender_details', tender_id=tender.id))


@tenders_bp.route('/<int:tender_id>/extract_data', methods=['GET', 'POST'])
@login_required
def extract_data(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    unit_price_form = UnitPriceForm()
    unit_price_form.id_oferty.data = tender.id

    extracted_text = tender.extracted_content or ""
    table_data = [] # This is not stored, so it will be empty
    is_image_file = tender.original_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))

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
            return redirect(url_for('tenders.extract_data', tender_id=tender.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania pozycji cenowej: {e}', 'danger')

    return render_template('extract_helper.html', 
                           tender=tender, 
                           extracted_text=extracted_text, 
                           table_data=table_data, 
                           unit_price_form=unit_price_form, 
                           categories=Category.query.order_by(Category.nazwa_kategorii).all(), 
                           unit_prices=tender.unit_prices.all(), 
                           title="Ekstrakcja danych z oferty",
                           is_image_file=is_image_file)

@tenders_bp.route('/<int:tender_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tender(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    form = TenderForm(obj=tender)
    
    if form.validate_on_submit():
        storage_service = get_storage_service()
        file_changed = False

        if form.delete_existing_file.data and not form.plik_oferty.data:
            if tender.storage_path:
                try:
                    storage_service.delete(tender.storage_path)
                    tender.original_filename = None
                    tender.storage_path = None
                    tender.file_type = None
                    tender.extracted_content = None
                    file_changed = True
                    flash('Istniejący plik został usunięty.', 'info')
                except Exception as e:
                    flash(f"Błąd podczas usuwania pliku: {e}", "danger")

        if form.plik_oferty.data:
            plik = form.plik_oferty.data
            filename = secure_filename(plik.filename)
            
            if tender.storage_path:
                try:
                    storage_service.delete(tender.storage_path)
                except Exception as e:
                    flash(f"Nie udało się usunąć starego pliku, ale kontynuowano wgrywanie nowego. Błąd: {e}", "warning")

            try:
                tender.storage_path = storage_service.upload(plik.stream, filename, plik.mimetype)
                tender.original_filename = filename
                tender.file_type = plik.mimetype
                file_changed = True
            except Exception as e:
                flash(f"Błąd podczas wgrywania nowego pliku: {e}", "danger")
                return redirect(url_for('tenders.edit_tender', tender_id=tender.id))

        tender.nazwa_oferty = form.nazwa_oferty.data
        tender.data_otrzymania = form.data_otrzymania.data
        tender.status = form.status.data
        tender.id_firmy = form.id_firmy.data
        tender.id_projektu = form.id_projektu.data if form.id_projektu.data else None
        
        db.session.commit()

        if file_changed:
            extract_and_save_text(tender)

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
            flash(f"Nie udało się usunąć pliku powiązanego z ofertą z GCS, ale oferta zostanie usunięta. Błąd: {e}", "warning")

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

                extract_and_save_text(nowa_oferta)

                flash('Nowa oferta została dodana pomyślnie!', 'success')
                return redirect(url_for('tenders.list_tenders'))

            except Exception as e:
                flash(f"Wystąpił błąd podczas przesyłania pliku: {e}", "danger")

        else:
            flash('Proszę załączyć plik oferty.', 'danger')
            
    return render_template('tender_form.html', form=form, title='Nowa Oferta')

# ... (reszta bez zmian)
