import json, logging
from app import app, db
from models import BibleVersion, Verse

def seed_database(json_path):
    with open(json_path, 'r', encoding = 'utf-8') as f:
        content = json.load(f)

    # open the app to populate database
    logging.debug('Opening app to populate database...')
    with app.app_context():
        db.create_all()
        v_meta = content['metadata']

        version = BibleVersion.query.filter_by(abbreviation = v_meta['abbreviation']).first()
        if(not version):
            version = BibleVersion(
                        abbreviation        = v_meta['abbreviation'],
                        title_full          = v_meta['title_full'],
                        verse_system        = v_meta['verse_system'],
                        language_code       = v_meta['language_code'],
                        copyright           = v_meta['copyright'],
                        description         = v_meta['description'],
                        # TODO: Find a way to add date either automatically or JSON data // might throw exceptions
                        publication_date    = None,
                    )
            db.session.add(version)
            db.session.commit()
            logging.debug(f'Succesfully added version {v_meta["abbreviation"]}!')
        else:
            logging.debug(f'Version {v_meta["abbreviation"]} already exists!')

        version = BibleVersion.query.filter_by(abbreviation = v_meta['abbreviation']).first()
        version_id = version.id
        logging.debug(f'Found id {version_id} for version {version.title_full}!')

        for verse in content['verses']:
            try:
                logging.debug(f'Adding verse {verse["uvid"]}...')
                new_verse = Verse(
                        version_id  = version_id, # TODO: Extract v_id from 'version'
                        uvid        = verse['uvid'],
                        # book_code   = verse['book_code'],
                        chapter     = verse['chapter'],
                        verse       = verse['verse'],
                        text        = verse['text'],
                        pericope    = verse['pericope'] 
                    )

                db.session.add(new_verse)
            except Exception as e:
                logging.error(e)
                return 1

            db.session.commit()

def main(verbose):
    if(verbose):
        logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    else:
        logging.basicConfig(level = logging.WARNING) # Only show errors by default

    logging.debug(f'Opening file...')
    seed_database('data/esperanto.json')

if(__name__ == '__main__'):
    main(1)
