from spotifest import app, db
from spotifest.columns import Festival, FestivalBand, Band
from flask import jsonify
from spotifest.spotify_api import CreatePlaylist
from spotifest.songkick_scrap import FestivalScraper

# TODO: Fix bad requests send back status codes.
# TODO: being able to add festivals/bands to the database, if authenticated.
# TODO: Vart ska denna filen ligga? I en egen mapp? I en egen app? I en egen app i en egen mapp?
# TODO: Fråga andreas vad alembic version är.
# TODO: control the scraper with a route with dev privileges


@app.route('/festivals/<festival>/create-playlist', methods=['GET'])
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




# TODO: Make route for api instructions. (GET)
@app.route('/', methods=['GET'])
def api_instructions():
    info_dict = {
        "info": "This is the API for Spotifest. It is currently under development.",
        "supported country codes": "se, uk, us, au, de, ca, br, id, es, nl, fr, mx, it, ar, ie",
        "endpoints": {
            "Get festivals in country": "/countries/<insert country code>",
            "Get information about the festival": "/festivals/<insert festival here>",
            "Creates playlist from selected festival": "/<insert festival here>/create-playlist",


        }
    }

    return jsonify(info_dict)


# This route adds a custom festival to the database.
@app.route('/database/Jacobs Backyard', methods=['GET'])
def add_festival():
    festival_dict = {
        "name": "Jacobs Backyard",
        "date": "09/09/09",
        "venue": "Bajspalatset",
        "bands": ["Minpipa", "Agusa", "Jesus"],
        "country": "ar"
    }

    new_festival = FestivalScraper()
    new_festival.add_festival_to_db(festival_dict)
    new_festival.add_band_to_db(festival_dict)

    success = {
        "success": f"Added {festival_dict['name']} to database successfully"
    }

    return jsonify(success, festival_dict)

# add scraper route here


