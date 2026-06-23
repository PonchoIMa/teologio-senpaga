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

class Resource(db.Model):
    # identifiers
    id                  = db.Column(db.Integer, primary_key = True) 
    resource_id         = db.Column(db.String(50), nullable = False, unique = True)

    # metadata
    author_family       = db.Column(db.String(30), nullable = False)
    author_given        = db.Column(db.String(20))
    publication_year    = db.Column(db.Integer)
    publication_month   = db.Column(db.String(10))
    publication_day     = db.Column(db.Integer)
    title               = db.Column(db.String(80), nullable = False)
    publisher           = db.Column(db.String(50))
    location            = db.Column(db.String(50))
    isbn13              = db.Column(db.String(13))
    url                 = db.Column(db.String(120))

    # relationships
    milestones          = db.relationship('ResourceLink', backref = 'resource_meta', lazy = True)

class Verse(db.Model):
    # identifiers
    id            = db.Column(db.Integer, primary_key = True) 
    version_id    = db.Column(db.Integer, db.ForeignKey('bible_version.id'), nullable = False) 

    # universal verse id - to identify the text to be cited.
    uvid        = db.Column(db.String(20), index = True, nullable = False)

    book_name   = db.Column(db.String(50), nullable = False) 
    chapter     = db.Column(db.Integer, nullable = False) 
    verse       = db.Column(db.Integer, nullable = False) 
    text        = db.Column(db.Text, nullable = False) 
    pericope    = db.Column(db.String(255))

class ResourceLink(db.Model):
    # identifier
    id          = db.Column(db.Integer, primary_key = True)

    # resource linking
    uvid        = db.Column(db.String(20), index = True, nullable = False)
    resource_id = db.Column(db.String(50), db.ForeignKey('resource.resource_id'), nullable = False)
    milestone   = db.Column(db.String(40), nullable = False)

# TODO: Tables for topics
