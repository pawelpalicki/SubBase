from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required
from app import db
from app.models import Tender
from app.forms import TenderForm
import os
from werkzeug.utils import secure_filename

tenders_bp = Blueprint('tenders', __name__, template_folder='templates', url_prefix='/tenders')

@tenders_bp.route('/')
@login_required
def list_tenders():
    tenders = Tender.query.order_by(Tender.data_otrzymania.desc()).all()
    return render_template('tenders_list.html', tenders=tenders, title='Oferty')

@tenders_bp.route('/<int:tender_id>')
@login_required
def tender_details(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    return render_template('tender_details.html', tender=tender, title=f"Szczegóły oferty: {tender.nazwa_oferty}")

@tenders_bp.route('/download/<int:tender_id>')
@login_required
def download_file(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    directory = current_app.config['UPLOAD_FOLDER']
    filename = tender.original_filename
    return send_from_directory(directory, filename, as_attachment=True)

@tenders_bp.route('/<int:tender_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tender(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    form = TenderForm(obj=tender)
    
    if form.validate_on_submit():
        tender.nazwa_oferty = form.nazwa_oferty.data
        tender.data_otrzymania = form.data_otrzymania.data
        tender.status = form.status.data
        tender.id_firmy = form.id_firmy.data
        
        # Sprawdź, czy użytkownik wgrał nowy plik
        if form.plik_oferty.data:
            plik = form.plik_oferty.data
            filename = secure_filename(plik.filename)
            
            # Opcjonalnie: usuń stary plik, jeśli istnieje
            if tender.storage_path and os.path.exists(tender.storage_path):
                os.remove(tender.storage_path)

            # Zapisz nowy plik
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            plik.save(upload_path)
            
            # Zaktualizuj dane pliku w modelu
            tender.original_filename = filename
            tender.storage_path = upload_path
            tender.file_type = plik.mimetype

        db.session.commit()
        flash('Oferta została zaktualizowana.', 'success')
        return redirect(url_for('tenders.tender_details', tender_id=tender.id))

    return render_template('tender_form.html', form=form, title=f"Edycja oferty: {tender.nazwa_oferty}")

@tenders_bp.route('/<int:tender_id>/delete', methods=['POST'])
@login_required
def delete_tender(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    
    # Usuń plik z serwera, jeśli istnieje
    if tender.storage_path and os.path.exists(tender.storage_path):
        os.remove(tender.storage_path)
        
    db.session.delete(tender)
    db.session.commit()
    flash('Oferta została usunięta.', 'success')
    return redirect(url_for('tenders.list_tenders'))

@tenders_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_tender():
    form = TenderForm()
    if form.validate_on_submit():
        plik = form.plik_oferty.data
        filename = secure_filename(plik.filename)
        
        # Zapisz plik w skonfigurowanym folderze
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        plik.save(upload_path)

        # Utwórz nowy obiekt Tender
        nowa_oferta = Tender(
            nazwa_oferty=form.nazwa_oferty.data,
            data_otrzymania=form.data_otrzymania.data,
            status=form.status.data,
            id_firmy=form.id_firmy.data,
            original_filename=filename,
            storage_path=upload_path, # Na razie przechowujemy lokalną ścieżkę
            file_type=plik.mimetype
        )
        
        db.session.add(nowa_oferta)
        db.session.commit()
        
        flash('Nowa oferta została dodana pomyślnie!', 'success')
        return redirect(url_for('tenders.list_tenders'))
        
    return render_template('tender_form.html', form=form, title='Nowa Oferta')
