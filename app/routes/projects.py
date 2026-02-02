from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import db
from app.models import Project
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from . import main

@main.route('/projects')
@login_required
def list_projects():
    projects = Project.query.all()
    return render_template('projects.html', items=projects, title='Projekty')

@main.route('/projects/new', methods=['GET', 'POST'])
@login_required
def new_project():
    from app.forms import ProjectForm
    form = ProjectForm()
    if form.validate_on_submit():
        try:
            new_project = Project(
                nazwa_projektu=form.nazwa_projektu.data,
                skrot=form.skrot.data,
                rodzaj=form.rodzaj.data,
                uwagi=form.uwagi.data
            )
            db.session.add(new_project)
            db.session.commit()
            flash('Projekt został dodany pomyślnie!', 'success')
            return redirect(url_for('main.list_projects'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas dodawania projektu: {e}', 'danger')
    return render_template('project_form.html', form=form, title='Dodaj Projekt', back_url=url_for('main.list_projects'))

@main.route('/api/projects', methods=['GET', 'POST'])
@login_required
def add_project_api():
    from app.forms import ProjectForm
    form = ProjectForm()
    if request.method == 'POST': # Explicitly check for POST
        if form.validate_on_submit():
            try:
                existing = Project.query.filter(func.lower(Project.nazwa_projektu) == func.lower(form.nazwa_projektu.data)).first()
                if existing:
                    return jsonify({'success': False, 'errors': {'nazwa_projektu': ['Projekt o tej nazwie już istnieje.']}}), 400
                new_project = Project(
                    nazwa_projektu=form.nazwa_projektu.data,
                    skrot=form.skrot.data,
                    rodzaj=form.rodzaj.data,
                    uwagi=form.uwagi.data
                )
                db.session.add(new_project)
                db.session.commit()
                return jsonify({'success': True, 'id': new_project.id, 'name': new_project.nazwa_projektu}), 201
            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({'success': False, 'errors': {'_form': [f'Błąd bazy danych: {str(e)}']}}), 500
        else: # Validation failed for POST request
            return jsonify({'success': False, 'errors': form.errors}), 400
    # For GET request
    return render_template('project_form_modal.html', form=form)

@main.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    from app.forms import ProjectForm
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        try:
            project.nazwa_projektu = form.nazwa_projektu.data
            project.skrot = form.skrot.data
            project.rodzaj = form.rodzaj.data
            project.uwagi = form.uwagi.data
            db.session.commit()
            flash('Projekt został zaktualizowany pomyślnie!', 'success')
            return redirect(url_for('main.list_projects'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Wystąpił błąd podczas aktualizacji projektu: {e}', 'danger')
    if request.method == 'GET':
        form.nazwa_projektu.data = project.nazwa_projektu
        form.skrot.data = project.skrot
        form.rodzaj.data = project.rodzaj
        form.uwagi.data = project.uwagi
    return render_template('project_form.html', form=form, title='Edytuj Projekt', back_url=url_for('main.list_projects'))

@main.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Projekt został usunięty pomyślnie!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Wystąpił błąd podczas usuwania projektu: {e}', 'danger')
    return redirect(url_for('main.list_projects'))
