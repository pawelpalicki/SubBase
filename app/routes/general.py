from flask import render_template, redirect, url_for
from flask_login import login_required
from . import main

@main.route('/')
@main.route('/index')
@login_required 
def index():
    return redirect(url_for('main.list_companies'))

@main.route('/instrukcja')
@login_required
def instruction():
    return render_template('instrukcja.html', title='Instrukcja')
