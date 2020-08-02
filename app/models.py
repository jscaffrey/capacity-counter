from app import db
import click
from flask.cli import with_appcontext

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

#Create a prompt for at least one location entry
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
