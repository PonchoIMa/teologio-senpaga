from flask import Flask, render_template
from models import db, Verse

app = Flask(__name__)

# libereco is 'freedom' in Esperanto, which is what this software aims to have once completed
# I want for tsp to be the one FOSS that everyone tunes into to do bullet bible study and without
# paywalls, ads or any other income except for human kindness, contributions and prayers.
# At the end, this has been, is, and forever shall be for the Glory of God alone (1 Co. 13.10)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libereco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/study/verse/<uvid>')
def study_verse(uvid):
    # Fetch data
    verse = Verse.query.filter_by(uvid = uvid).first_or_404()
    
    # TODO: Add to Adamo verse.topics and verse.resources
    return render_template('study_verse.html', verse = verse)
