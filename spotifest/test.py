from spotifest import app, db
from spotifest.models import Festival, FestivalBand, Band
from flask import url_for
from flask import jsonify
from json import dumps
with app.app_context():
    bands = FestivalBand.query.filter_by(festival_name="Subkultfestivalen").all()

    print(bands)