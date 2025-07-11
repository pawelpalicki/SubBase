from app import db

class Firmy(db.Model):
    __tablename__ = 'firmy'
    id_firmy = db.Column(db.Integer, primary_key=True)
    nazwa_firmy = db.Column(db.Text)
    id_firmy_typ = db.Column(db.Integer, db.ForeignKey('firmy_typ.id_firmy_typ'))
    strona_www = db.Column(db.Text)
    uwagi = db.Column(db.Text)
    
    adresy = db.relationship('Adresy', backref='firma', lazy='dynamic')
    emails = db.relationship('Email', backref='firma', lazy='dynamic')
    telefony = db.relationship('Telefon', backref='firma', lazy='dynamic')
    osoby = db.relationship('Osoby', backref='firma', lazy='dynamic')
    oceny = db.relationship('Oceny', backref='firma', lazy='dynamic')
    
    firmy_specjalnosci = db.relationship('FirmySpecjalnosci', backref='firma', lazy='dynamic')
    firmy_obszar_dzialania = db.relationship('FirmyObszarDzialania', backref='firma', lazy='dynamic')
    tenders = db.relationship('Tender', backref='firma', lazy='dynamic')

class FirmyTyp(db.Model):
    __tablename__ = 'firmy_typ'
    id_firmy_typ = db.Column(db.Integer, primary_key=True)
    typ_firmy = db.Column(db.Text)
    
    firmy = db.relationship('Firmy', backref='typ_firmy', lazy='dynamic')

class AdresyTyp(db.Model):
    __tablename__ = 'adresy_typ'
    id_adresy_typ = db.Column(db.Integer, primary_key=True)
    typ_adresu = db.Column(db.Text)
    
    adresy = db.relationship('Adresy', backref='typ_adresu', lazy='dynamic')

class Adresy(db.Model):
    __tablename__ = 'adresy'
    id_adresy = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kod = db.Column(db.Text)
    miejscowosc = db.Column(db.Text)
    ulica_miejscowosc = db.Column(db.Text)
    id_adresy_typ = db.Column(db.Integer, db.ForeignKey('adresy_typ.id_adresy_typ'))
    id_firmy = db.Column(db.Integer, db.ForeignKey('firmy.id_firmy'))

class EmailTyp(db.Model):
    __tablename__ = 'email_typ'
    id_email_typ = db.Column(db.Integer, primary_key=True)
    typ_emaila = db.Column(db.Text)
    
    emails = db.relationship('Email', backref='typ_emaila', lazy='dynamic')

class Email(db.Model):
    __tablename__ = 'email'
    id_email = db.Column(db.Integer, primary_key=True)
    e_mail = db.Column(db.Text)
    id_email_typ = db.Column(db.Integer, db.ForeignKey('email_typ.id_email_typ'))
    id_firmy = db.Column(db.Integer, db.ForeignKey('firmy.id_firmy'))

class TelefonTyp(db.Model):
    __tablename__ = 'telefon_typ'
    id_telefon_typ = db.Column(db.Integer, primary_key=True)
    typ_telefonu = db.Column(db.Text)
    
    telefony = db.relationship('Telefon', backref='typ_telefonu', lazy='dynamic')

class Telefon(db.Model):
    __tablename__ = 'telefon'
    id_telefon = db.Column(db.Integer, primary_key=True)
    telefon = db.Column(db.Text)
    id_telefon_typ = db.Column(db.Integer, db.ForeignKey('telefon_typ.id_telefon_typ'))
    id_firmy = db.Column(db.Integer, db.ForeignKey('firmy.id_firmy'))

class Specjalnosci(db.Model):
    __tablename__ = 'specjalnosci'
    id_specjalnosci = db.Column(db.Integer, primary_key=True)
    specjalnosc = db.Column(db.Text)
    
    firmy_specjalnosci = db.relationship('FirmySpecjalnosci', backref='specjalnosc', lazy='dynamic')

class FirmySpecjalnosci(db.Model):
    __tablename__ = 'firmyspecjalnosci'
    id_firmy = db.Column(db.Integer, db.ForeignKey('firmy.id_firmy'), primary_key=True)
    id_specjalnosci = db.Column(db.Integer, db.ForeignKey('specjalnosci.id_specjalnosci'), primary_key=True)

class Kraj(db.Model):
    __tablename__ = 'kraj'
    id_kraj = db.Column(db.Text, primary_key=True)
    kraj = db.Column(db.Text)
    
    firmy_obszar_dzialania = db.relationship('FirmyObszarDzialania', backref='kraj', lazy='dynamic')

class Wojewodztwa(db.Model):
    __tablename__ = 'wojewodztwa'
    id_wojewodztwa = db.Column(db.Text, primary_key=True)
    wojewodztwo = db.Column(db.Text)
    
    powiaty = db.relationship('Powiaty', backref='wojewodztwo', lazy='dynamic')
    firmy_obszar_dzialania = db.relationship('FirmyObszarDzialania', backref='wojewodztwo', lazy='dynamic')

class Powiaty(db.Model):
    __tablename__ = 'powiaty'
    id_powiaty = db.Column(db.Integer, primary_key=True)
    powiat = db.Column(db.Text)
    id_wojewodztwa = db.Column(db.Text, db.ForeignKey('wojewodztwa.id_wojewodztwa'))
    
    firmy_obszar_dzialania = db.relationship('FirmyObszarDzialania', backref='powiat', lazy='dynamic')

class FirmyObszarDzialania(db.Model):
    __tablename__ = 'firmyobszardzialania'
    id_firmy = db.Column(db.Integer, db.ForeignKey('firmy.id_firmy'), primary_key=True)
    id_kraj = db.Column(db.Text, db.ForeignKey('kraj.id_kraj'), primary_key=True)
    id_wojewodztwa = db.Column(db.Text, db.ForeignKey('wojewodztwa.id_wojewodztwa'), primary_key=True)
    id_powiaty = db.Column(db.Integer, db.ForeignKey('powiaty.id_powiaty'), primary_key=True)

class Osoby(db.Model):
    __tablename__ = 'osoby'
    id_osoby = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.Text)
    nazwisko = db.Column(db.Text)
    stanowisko = db.Column(db.Text)
    e_mail = db.Column(db.Text)
    telefon = db.Column(db.Text)
    id_firmy = db.Column(db.Integer, db.ForeignKey('firmy.id_firmy'))

class Oceny(db.Model):
    __tablename__ = 'oceny'
    oceny_id = db.Column(db.Integer, primary_key=True)
    osoba_oceniajaca = db.Column(db.Text)
    budowa_dzial = db.Column(db.Text)
    rok_wspolpracy = db.Column(db.Integer)
    ocena = db.Column(db.Integer)
    komentarz = db.Column(db.Text)
    id_firmy = db.Column(db.Integer, db.ForeignKey('firmy.id_firmy'))

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    nazwa_projektu = db.Column(db.String(255), nullable=False, unique=True)
    skrot = db.Column(db.String(50), nullable=True)
    rodzaj = db.Column(db.String(50), nullable=True)
    uwagi = db.Column(db.Text, nullable=True)
    tenders = db.relationship('Tender', backref='project', lazy='dynamic')

class Tender(db.Model):
    __tablename__ = 'tenders'
    id = db.Column(db.Integer, primary_key=True)
    nazwa_oferty = db.Column(db.String(255), nullable=False)
    data_otrzymania = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Nowa')
    original_filename = db.Column(db.String(255))
    storage_path = db.Column(db.String(1024))
    file_type = db.Column(db.String(100))
    id_firmy = db.Column(db.Integer, db.ForeignKey('firmy.id_firmy'), nullable=False)
    id_projektu = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    unit_prices = db.relationship('UnitPrice', backref='tender', lazy='dynamic')

class WorkType(db.Model):
    __tablename__ = 'work_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    id_kategorii = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', backref='work_types')
    unit_prices = db.relationship('UnitPrice', backref='work_type', lazy='dynamic')

class UnitPrice(db.Model):
    __tablename__ = 'unit_prices'
    id = db.Column(db.Integer, primary_key=True)
    id_work_type = db.Column(db.Integer, db.ForeignKey('work_types.id'), nullable=False)
    jednostka_miary = db.Column(db.String(50), nullable=False)
    cena_jednostkowa = db.Column(db.Numeric(10, 2), nullable=False)
    id_oferty = db.Column(db.Integer, db.ForeignKey('tenders.id'), nullable=False)
    id_kategorii = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='unit_prices')
    uwagi = db.Column(db.Text, nullable=True)
    # Pole nazwa_roboty zostanie usunięte po migracji danych
    nazwa_roboty = db.Column(db.String(255), nullable=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    nazwa_kategorii = db.Column(db.String(255), nullable=False, unique=True)