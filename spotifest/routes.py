from spotifest import app, db
from spotifest.columns import Festival, FestivalBand, Band
from flask import url_for
from flask import jsonify
from json import dumps
from spotifest.spotify_api import CreatePlaylist


@app.route('/<festival>/create-playlist', methods=['GET'])
def create_playlist(festival):

    bands_in_playlist = [ band.band_name for band in FestivalBand.query.filter_by(festival_name=festival).all() ]
    new_playlist = CreatePlaylist(festival=festival, bands=bands_in_playlist)
    playlist_url = new_playlist.create_playlist()
    playlist = {
        "playlist_url": f"https://open.spotify.com/playlist/{playlist_url}"
    }

    return jsonify(playlist)


@app.route('/countries/<country>', methods=['GET'])
def get_festivals(country):

    fest_dict = {}
    festivals = Festival.query.filter_by(country=country).all()

    for j in range(len(festivals)):
        fest_dict[j] = {
            "name": festivals[j].name,
            "date": festivals[j].date,
            "venue": festivals[j].venue,
        }

    return jsonify(fest_dict)


# # Returns json with festival info
@app.route('/festivals/<festival>', methods=['GET'])
def get_bands(festival):

    bands = FestivalBand.query.filter_by(festival_name=festival).all()
    band_dict = {}
    for j in range(len(bands)):
        band_dict[j] = {
            "name": bands[j].band_name,
            "festival": bands[j].festival_name,
        }

    return jsonify(band_dict)

# # /band/info
# # Returns json with band information
# @app.route('/band/info', methods=['GET'])


# TODO: Make route for api instructions. (GET)
@app.route('/', methods=['GET'])
def api_instructions():
    info_dict = {
        "info": "This is the API for Spotifest. It is currently under development.",
        "endpoints": {
            "country": "/{country_code}",
            "supported countries": "se, uk, us",
            "festival/info": "/festival/info",
            "band/info": "/band/info"

        }
    }

    return jsonify(info_dict)



