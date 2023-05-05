from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

# The application instance is created as an instance of class Flask in the __init__.py script, at the top-level.
app = Flask(__name__)
# The config.py file is imported and the app.config.from_object() method is used to load the configuration from the config.py file.
app.config.from_object(Config)
# The database instance is created as an instance of class SQLAlchemy in the __init__.py script, at the top-level.
db = SQLAlchemy(app)
# The migrate instance is created as an instance of class Migrate in the __init__.py script, at the top-level.
migrate = Migrate(app, db)

SWAGGER_URL = '/swagger'
API_URL = '/static/Spotifest.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Spotifest API"
    })


app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

from spotifest import routes, models
