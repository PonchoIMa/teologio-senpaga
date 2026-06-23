import json, logging, argparse
from app import app, db
from models import BibleVersion, Verse, Resource, ResourceLink

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
                        version_id  = version_id, 
                        uvid        = verse['uvid'],
                        book_name   = verse['book_name'],
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

def index(filepath):
    with open(filepath, 'r', encoding = 'utf-8') as f:
        content = json.load(f)

    # open the app to populate database
    logging.debug('Opening app to populate database...')
    with app.app_context():
        db.create_all()
        resource_meta = content['metadata']

        resource = Resource.query.filter_by(resource_id = resource_meta['resource_id']).first()
        if(not resource):
            resource = Resource(
                resource_id         = resource_meta['resource_id'],
                author_family       = resource_meta['author_family'],
                author_given        = resource_meta['author_given'],
                publication_year    = resource_meta['publication_year'],
                publication_month   = resource_meta['publication_month'],
                publication_day     = resource_meta['publication_day'],
                title               = resource_meta['title'],
                publisher           = resource_meta['publisher'],
                location            = resource_meta['location'],
                isbn13              = resource_meta['isbn13'],
                url                 = resource_meta['url']
            )
            db.session.add(resource)
            db.session.commit()
            logging.debug(f'Succesfully added resource {resource_meta["resource_id"]}!')
        else:
            logging.debug(f'Resource {resource_meta["resource_id"]} already exists!')

        resource = Resource.query.filter_by(resource_id = resource_meta['resource_id']).first()
        resource_id = resource.resource_id
        logging.debug(f'Found id {resource_id} for version {resource.title}!')

        for segment in content['segments']:
            try:
                logging.debug(f'Adding link {segment["id"]}...')
                if(len(segment['uvid_links']) > 1):
                    for link in segment['uvid_links']:
                        new_link = ResourceLink(
                            uvid        = link,
                            resource_id = resource_id,
                            milestone   = segment['id']
                        )

                        db.session.add(new_link)
                else:
                    new_link = ResourceLink(
                        uvid        = segment['uvid_links'][0],
                        resource_id = resource_id,
                        milestone   = segment['id']
                    )

                    db.session.add(new_link)
            except Exception as e:
                logging.error(e)
                return 1

            db.session.commit()

def main(verbose, filepaths):
    if(verbose):
        logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    else:
        logging.basicConfig(level = logging.WARNING) # Only show errors by default

    # Loop through all files passed via the -f argument
    for filepath in filepaths:
        logging.debug(f'Opening file {filepath}...')
        
        # Read the file briefly to peek at its structure
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = json.load(f)
        except Exception as e:
            logging.error(f"Could not read {filepath}: {e}")
            continue

        # Route the file to the correct database function
        if 'verses' in content:
            logging.debug(f'Detected Bible text format. Sending to seed_database()...')
            seed_database(filepath)
        elif 'segments' in content:
            logging.debug(f'Detected Commentary/Resource format. Sending to index()...')
            index(filepath)
        else:
            logging.warning(f'Unknown file structure in {filepath}. Skipping.')

"""
def main(verbose, filepath):
    if(verbose):
        logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    else:
        logging.basicConfig(level = logging.WARNING) # Only show errors by default

    logging.debug(f'Opening file...')
    index(filepath[0])
"""

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(
            prog        = 'seeder.py',
            description = 'a simple database seeder',
            epilog      = 'made with <3 by ponchoima')

    parser.add_argument('-f', '--files', nargs = '+', required = True,
                        help = 'path(s) for file(s) to parse (supports wildcards like *.utf)')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False,
                        help = 'outputs the steps it follows')

    args = parser.parse_args()
    main(args.verbose, args.files)
