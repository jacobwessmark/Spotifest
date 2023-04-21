from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# The application instance is created as an instance of class Flask in the __init__.py script, at the top-level.
app = Flask(__name__)
# The config.py file is imported and the app.config.from_object() method is used to load the configuration from the config.py file.
app.config.from_object(Config)
# The database instance is created as an instance of class SQLAlchemy in the __init__.py script, at the top-level.
db = SQLAlchemy(app)
# The migrate instance is created as an instance of class Migrate in the __init__.py script, at the top-level.
migrate = Migrate(app, db)

from spotifest import routes, columns