from app import db, login
import click
from flask_login import UserMixin
from flask.cli import with_appcontext
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(UserMixin, db.Model, Base):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(128))
    user_settings = relationship("UserSettings",\
            uselist=False,\
            back_populates="user")

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

class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(128))
    url = db.Column(db.String(512))
    weight = db.Column(db.Integer)

class UserSettings(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    dark_mode = db.Column(db.Boolean, nullable=False, default=False)
    last_activity = db.Column(db.DateTime)
    on_duty = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="user_settings")

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

#Create a command line prompt for a link entry
@click.command("add-link", help='Adds a link to the navigation')
@click.option('--label', prompt=True)
@click.option('--url', prompt=True)
@click.option('--weight', prompt=True)
@with_appcontext
def add_link(label, url, weight):
    if weight is None:
        weight = ""
    link = Links(label=label, url=url, weight=weight)
    db.session.add(link)
    db.session.commit()
    click.echo("Link created.")
