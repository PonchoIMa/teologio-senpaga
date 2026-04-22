import json
from app import app, db
from models import BibleVersion, Verse

def seed_database(json_path):
    with open(json_path, 'r', encoding = 'utf-8') as f:
        content = json.load(f)

    # open the app to populate database
    with app.app_context():
        db.create_all()
        v_meta = content['metadata'][... # TODO: Pair with curated json, models and query
