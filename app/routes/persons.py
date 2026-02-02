from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Osoby, Oceny
from sqlalchemy.exc import SQLAlchemyError
from . import main

# Routes for Persons

@main.route('/persons')
@login_required
def list_persons():
    persons = Osoby.query.all()
    return render_template('persons.html', items=persons, title='Osoby Kontaktowe')

@main.route('/persons/new', methods=['GET', 'POST'])
@login_required
def new_person():
    from app.forms import SimplePersonForm
    form = SimplePersonForm()
    if form.validate_on_submit():
        try:
            new_person = Osoby(
                imie=form.imie.data,
                nazwisko=form.nazwisko.data,
                stanowisko=form.stanowisko.data,
                e_mail=form.e_mail.data,
                telefon=form.telefon.data,
                id_firmy=form.id_firmy.data
            )
            db.session.add(new_person)
            db.session.commit()
            flash('Osoba kontaktowa została dodana pomyślnie!', 'success')
            return redirect(url_for('main.list_persons'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania osoby kontaktowej: {e}', 'danger')
    return render_template('person_form.html', form=form, title='Dodaj Osobę Kontaktową', back_url=url_for('main.list_persons'))

@main.route('/persons/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_person(id):
    from app.forms import SimplePersonForm
    person = Osoby.query.get_or_404(id)
    form = SimplePersonForm(obj=person)

    if form.validate_on_submit():
        try:
            person.imie = form.imie.data
            person.nazwisko = form.nazwisko.data
            person.stanowisko = form.stanowisko.data
            person.e_mail = form.e_mail.data
            person.telefon = form.telefon.data
            person.id_firmy = form.id_firmy.data
            db.session.commit()
            flash('Osoba kontaktowa została zaktualizowana pomyślnie!', 'success')
            return redirect(url_for('main.list_persons'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas aktualizacji osoby kontaktowej: {e}', 'danger')

    return render_template('person_form.html', form=form, title='Edytuj Osobę Kontaktową', back_url=url_for('main.list_persons'))

@main.route('/persons/<int:id>/delete', methods=['POST'])
@login_required
def delete_person(id):
    person = Osoby.query.get_or_404(id)
    try:
        db.session.delete(person)
        db.session.commit()
        flash('Osoba kontaktowa została usunięta pomyślnie!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania osoby kontaktowej: {e}', 'danger')
    return redirect(url_for('main.list_persons'))

# Routes for Ratings

@main.route('/ratings')
@login_required
def list_ratings():
    ratings = Oceny.query.all()
    return render_template('ratings.html', items=ratings, title='Oceny Współpracy')

@main.route('/ratings/new', methods=['GET', 'POST'])
@login_required
def new_rating():
    from app.forms import SimpleRatingForm
    form = SimpleRatingForm()
    if form.validate_on_submit():
        try:
            new_rating = Oceny(
                osoba_oceniajaca=form.osoba_oceniajaca.data,
                budowa_dzial=form.budowa_dzial.data,
                rok_wspolpracy=form.rok_wspolpracy.data,
                ocena=form.ocena.data,
                komentarz=form.komentarz.data,
                id_firmy=form.id_firmy.data
            )
            db.session.add(new_rating)
            db.session.commit()
            flash('Ocena została dodana pomyślnie!', 'success')
            return redirect(url_for('main.list_ratings'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania oceny: {e}', 'danger')
    return render_template('rating_form.html', form=form, title='Dodaj Ocenę Współpracy', back_url=url_for('main.list_ratings'))

@main.route('/ratings/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_rating(id):
    from app.forms import SimpleRatingForm
    rating = Oceny.query.get_or_404(id)
    form = SimpleRatingForm(obj=rating)
    if form.validate_on_submit():
        try:
            rating.osoba_oceniajaca = form.osoba_oceniajaca.data
            rating.budowa_dzial = form.budowa_dzial.data
            rating.rok_wspolpracy = form.rok_wspolpracy.data
            rating.ocena = form.ocena.data
            rating.komentarz = form.komentarz.data
            rating.id_firmy = form.id_firmy.data
            db.session.commit()
            flash('Ocena została zaktualizowana pomyślnie!', 'success')
            return redirect(url_for('main.list_ratings'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas aktualizacji oceny: {e}', 'danger')
    return render_template('rating_form.html', form=form, title='Edytuj Ocenę Współpracy', back_url=url_for('main.list_ratings'))

@main.route('/ratings/<int:id>/delete', methods=['POST'])
@login_required
def delete_rating(id):
    rating = Oceny.query.get_or_404(id)
    try:
        db.session.delete(rating)
        db.session.commit()
        flash('Ocena została usunięta pomyślnie!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania oceny: {e}', 'danger')
    return redirect(url_for('main.list_ratings'))
