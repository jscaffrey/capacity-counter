#Flask application instance
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_envvar('CAPACITYCOUNTER_SETTINGS')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager()
login.init_app(app)

from app import routes, models, scheduler
app.cli.add_command(models.create_user)
app.cli.add_command(models.add_location)
app.cli.add_command(models.add_link)
