from app import db, login
import click
from flask_login import UserMixin
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    occupancy = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    occupancy_over_time = db.relationship("OccupancyOverTime", back_populates="location")

class OccupancyOverTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    occupancy = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location", back_populates="occupancy_over_time")

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#Create a command line prompt for creating user
@click.command("create-user", \
        help='Creates a user for the capacity counter')
@click.option('--name', prompt=True)
@click.option('--username', prompt=True)
@click.option('--passcode', prompt=True, hide_input=True,\
        confirmation_prompt=True)
@click.option('--admin', default=False, is_flag=True)
@with_appcontext
def create_user(name, username, passcode, admin):
    user = User(name=name, username=username, admin=admin)
    user.set_password(passcode)
    db.session.add(user)
    db.session.commit()
    click.echo("User created.")

#Create a command line prompt for a location entry
@click.command("add-location", help='Adds a location')
@click.option('--name', prompt=True)
@click.option('--capacity', prompt=True,
        confirmation_prompt=True, type=int)
@click.option('--description', prompt=False)
@with_appcontext
def add_location(name, capacity, description):
    if description is None:
        description = ""
    location = Location(name=name, capacity=capacity,\
            description=description, occupancy=0)
    db.session.add(location)
    db.session.commit()
    click.echo("Location created.")

