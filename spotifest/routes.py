# from spotifest import app, db
# from spotifest.columns import Festival, FestivalBand, Band
# from flask import url_for
#
#
# # /country
# # gives a list of all festivals in the country
# @app.route('/<country>', methods=['GET'])
# def get_festivals(country):
#     festivals = Festival.query.filter_by(country=country).all()
#     return festivals
#
#
# # /festival/info
# # Returns json with festival info
# @app.route('/festival/info', methods=['GET'])
#
#
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



