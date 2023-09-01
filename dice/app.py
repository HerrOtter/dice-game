
from flask import Flask

from .api import api
from .frontend import frontend
from .admin import admin
from .auth import login_manager
from .game import _game_context_processor
from .models import db
from .items import import_items

# Flask
app = Flask("dice")
app.register_blueprint(api)
app.register_blueprint(frontend)
app.url_map.strict_slashes = False

# Flask-SQLalchemy
app.secret_key = 'SECRET_DICE'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dice.db"
db.init_app(app)

# Flask-Admin
# https://bootswatch.com/3/
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'
admin.init_app(app)

# Flask-Login
login_manager.init_app(app)

# Init
with app.app_context():
    db.create_all()
import_items()
app.context_processor(_game_context_processor)
