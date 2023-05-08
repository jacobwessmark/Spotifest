import sqlalchemy.exc

from spotifest import app, db
from spotifest.models import Festival, FestivalBand, Band
from flask import jsonify, request
from spotifest.spotify_api import CreatePlaylist
from spotifest.db_add import FestivalCreator
from werkzeug.exceptions import BadRequest


# TODO: Fix bad requests send back status codes med try och except IF request.method == 'GET'.
# TODO: Skriv kommentarer
# TODO: Fixa ReadME filen så att Andreas vet hur han startar programmet och använder det från sin burk :) måste skapa databas med db init


@app.route('/', methods=['GET'])
def api_instructions():
    info_dict = {
        "info": f"For api documentation refer to /swagger"
        }

    return jsonify(info_dict)


@app.route('/festivals', methods=["GET"])
def get_festivals():
    try:
        if request.method == "GET":

            country = request.args.get('country')
            fest_list = []
            festivals = Festival.query.filter_by(country=country).all()
            if len(festivals):
                for j in range(len(festivals)):
                    festival = {
                        "name": festivals[j].name,
                        "date": festivals[j].date,
                        "venue": festivals[j].venue,
                    }
                    fest_list.append(festival)

                return jsonify(fest_list), 200
            else:
                return jsonify({"error": "No festivals found within that country, please refer to our supported "
                                         "countries at /swagger"}), 404

    except BadRequest as e:
        return jsonify({"error": e}), 400
    except sqlalchemy.exc.InvalidRequestError:
        return jsonify({"error": "Invalid Request"}), 400


@app.route('/festivals/<festival>', methods=['GET'])
def get_bands(festival):
    bands = FestivalBand.query.filter_by(festival_name=festival).all()
    band_list = []
    for j in range(len(bands)):
        band = {
            "name": bands[j].band_name,
            "festival": bands[j].festival_name,
        }
        band_list.append(band)
    return jsonify(band_list)


@app.route('/festivals/<festival>/create-playlist', methods=['GET'])
def create_playlist(festival):

    bands_in_playlist = [band.band_name for band in FestivalBand.query.filter_by(festival_name=festival).all()]
    if len(bands_in_playlist):
        new_playlist = CreatePlaylist(festival=festival, bands=bands_in_playlist)
        playlist_url = new_playlist.create_playlist()
        playlist = {
            "playlist_url": f"https://open.spotify.com/playlist/{playlist_url}"
        }
    else:
        return jsonify({"error": f"{festival} not found in database, if you want to add this festival go to:......"})

    return jsonify(playlist)


@app.route('/database', methods=['POST'])
def add_festival():
    # Här tar vi emot ett json-objekt med festivaldata
    festival_dict = request.json
    new_festival = FestivalCreator()
    new_festival.add_festival_to_db(festival_dict)
    new_festival.add_band_to_db(festival_dict)

    result = {
        "result": f"Added {festival_dict['name']} to database successfully"
    }

    return jsonify(result, festival_dict)



# This route uses the FestivalCreator class to scrape festivals from a country and add them to the database.
@app.route('/database/<country>', methods=['GET'])
def add_festivals(country):
    new_country = FestivalCreator(country=country)
    new_country.scrape_festivals_from_web()
    return jsonify({"result": f"Added festivals from {country} to database successfully"})
