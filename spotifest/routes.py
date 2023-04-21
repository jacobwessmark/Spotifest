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
#
#
# @app.route('/test', methods='GET')
# def hello():
#     return "hello world"
