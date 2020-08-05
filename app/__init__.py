#Flask application instance
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_envvar('CAPACITYCOUNTER_SETTINGS')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


from app import routes, models, occupancy_over_time
app.cli.add_command(models.create_admin)
app.cli.add_command(models.create_user)
app.cli.add_command(models.add_location)
