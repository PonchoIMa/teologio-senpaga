import json
from app import app, db
from models import BibleVersion, Verse

# TODO: Add logging!))

def seed_database(json_path):
    with open(json_path, 'r', encoding = 'utf-8') as f:
        content = json.load(f)

    # open the app to populate database
    with app.app_context():
        db.create_all()
        v_meta = content['metadata']

        version = BibleVersion.query.filter_by(abbreviation = v_meta['abbreviation']).first()
        if(not version):
            version = BibleVersion(
                        abbreviation        = v_meta['abbreviation'],
                        title_full          = v_meta['title_full'],
                        verse_system        = v_meta['verse_system'],
                        language_code       = v_meta['language'],
                        copyright           = v_meta['copyright'],
                        description         = 'lorem ipsum',
                        # TODO: Find a way to add date either automatically or JSON data // might throw exceptions
                        publication_date    = None,
                    )
            db.session.add(version)
            db.session.commit()

        for verse in content['verses']:
            try:
                new_verse = Verse(
                        version_id  = 'foo', # TODO: Extract v_id from 'version'
                        uvid        = verse['uvid'],
                        book_code   = verse['book_code'],
                        chapter     = verse['chapter'],
                        verse       = verse['verse'],
                        text        = verse['text'],
                        pericope    = verse['pericope'] 
                    )

                db.session.add(new_verse)
            except:
                pass

            db.session.commit()
