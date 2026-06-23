import os, json, logging, traceback
from scripts.verse_parser import uvid as uvid_parse
from flask import Flask, render_template, abort, request, redirect, url_for, session
from flask_babel import Babel
from models import db, Verse, Resource, ResourceLink

# Initial configuration
app     = Flask(__name__)

# Session configuration
app.secret_key = 'super-secret-key-to-change-in-productoin'

# Babel configuration - Esperanto is the main language, no turning back on that
app.config['BABEL_DEFAULT_LOCALE'] = 'eo'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC-6'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# Logging
logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')

def get_locale():
    # get lang from session:
    if('lang' in session):
        return session['lang']

    # url setting (manual testing)
    val = request.args.get('lang')
    if val in ['eo', 'en', 'es', 'ru']:
        return val

    # browser headers
    return request.accept_languages.best_match(['eo', 'en', 'es', 'ru'])

babel   = Babel(app, locale_selector = get_locale)

# libereco is 'freedom' in Esperanto, which is what this software aims to have once completed
# I want for tsp to be the one FOSS that everyone tunes into to do bullet bible study and without
# paywalls, ads or any other income except for human kindness, contributions and prayers.
# At the end, this has been, is, and forever shall be for the Glory of God alone (1 Co. 13.10)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libereco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/setlang/<lang_code>')
def set_language(lang_code):
    if lang_code in ['eo', 'en', 'es', 'ru']:
        session['lang'] = lang_code
        logging.debug(f"Session language permanently changed to: {lang_code}")
    
    # Redirect back to where the user came from, or homepage if it's missing
    return redirect(request.referrer or url_for('landing_page'))

@app.route('/study/verse/<uvid>')
def study_verse(uvid):
    # Fetch data
    verses_found    = Verse.query.filter_by(uvid = uvid).all()
    links           = ResourceLink.query.filter_by(uvid = uvid).all()
    
    if(not verses_found):
        abort(404)

    resolved_comments   = []
    loaded_books        = {}

    # dictionary mapping the abbreviation to the verse object
    available_versions = {v.version_meta.abbreviation: v for v in verses_found}
    requested_version = request.args.get('v')

    if(requested_version and requested_version in available_versions):
        anchor_verse = available_versions[requested_version]
    else:
        # fallback to Esperanto (ESP) if no version is requested, or the first available
        anchor_verse = available_versions.get('ESP', verses_found[0])
    
    # Gathering comments...
    for link in links:
        json_filename = f'data/books/{link.resource_id}.json'
        
        if json_filename not in loaded_books:
            try:
                with open(json_filename, 'r', encoding='utf-8') as f:
                    loaded_books[json_filename] = json.load(f)
            except Exception as e:
                logging.error(traceback.format_exc())
                continue  # Skip unreadable or missing files gracefully
        
        book_data = loaded_books.get(json_filename)
        if book_data:
            # Look for the exact milestone ID entry matching the database record
            for segment in book_data.get('segments', []):
                if(link.milestone in segment['id']):
                    resolved_comments.append({
                        'metadata': book_data['metadata'],
                        'segment_id': segment['id'],
                        'title': segment.get('title'),
                        'subtitle': segment.get('subtitle'),
                        'paragraph': segment.get('paragraph')
                    })
   
    # TODO: Add to Adamo verse.topics
    return render_template('study_verse.html',
                           verse                = anchor_verse,
                           available_versions   = available_versions,
                           comments             = resolved_comments)

@app.route('/')
def landing_page():
    # TODO: Remove verse (?)
    verse     = Verse.query.filter_by(uvid = "GEN.1.1").first_or_404()
    return render_template('index.html', verse = verse)

@app.route('/study', methods = ['GET'])
def searching_middle():
    query = request.args['q']

    # Assume verse first.
    if(request.args['q']):
        # TODO: Verse lookup
        return redirect(url_for('study_verse', uvid = uvid_parse(request.args['q'])))

    # TODO: Topic lookup

    # TODO: Remove verse (?)
    verse   = Verse.query.filter_by(uvid = "GEN.1.1").first_or_404()
    error   = 'Content: \'{}\' not found'
    return render_template('index.html', verse = verse)

