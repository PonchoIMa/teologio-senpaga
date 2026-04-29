from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BibleVersion(db.Model):
    # identifiers
    id            = db.Column(db.Integer, primary_key = True) 

    # abbreviation for the bible (NBLA, EO_LSB, etc...)
    abbreviation  = db.Column(db.String(10), unique = True, nullable = False) 
    title_full    = db.Column(db.String(255), nullable = False) 
    verse_system  = db.Column(db.String(30), nullable = False) 

    # for future implementation (eo, en, es, ru)
    language_code       = db.Column(db.String(5), nullable = False) 
    copyright           = db.Column(db.Text, nullable = False) 
    description         = db.Column(db.Text, nullable = False) 
    publication_date    = db.Column(db.Date) 

    # relationships
    verses        = db.relationship('Verse', backref = 'version_meta', lazy = True)

class Verse(db.Model):
    # identifiers
    id            = db.Column(db.Integer, primary_key = True) 
    version_id    = db.Column(db.Integer, db.ForeignKey('bible_version.id'), nullable = False) 

    # universal verse id - to identify the text to be cited.
    uvid        = db.Column(db.String(20), unique = True, nullable = False)

    # TODO: Create a curated book code list that the database can get
    # TODO: Sovle for this
    # book_code   = db.Column(db.String(5), nullable = False) 
    chapter     = db.Column(db.Integer, nullable = False) 
    verse       = db.Column(db.Integer, nullable = False) 
    text        = db.Column(db.Text, nullable = False) 
    pericope    = db.Column(db.String(255))

# TODO: Tables for topics and resources (milestones)
