#Home page route
from flask import render_template, request, jsonify, url_for
from app import app, db
from app.models import Location, OccupancyOverTime

@app.route('/')
@app.route('/index')
def index():
    location_id = request.args.get("id", 1)
    location = Location.query.filter_by(id=location_id).first()
    
    return render_template('index.html', title='Home', location=location)

@app.route('/increment')
def increment():
    location_id = request.args.get("id", 1)
    location = Location.query.filter_by(id=location_id).first()

    location.occupancy += 1

    db.session.commit()

    return str(location.occupancy)

@app.route('/decrement')
def decrement():
    location_id = request.args.get("id", 1)
    location = Location.query.filter_by(id=location_id).first()
    if location.occupancy > 0:
        location.occupancy -= 1

    db.session.commit()

    return str(location.occupancy)

@app.route('/location')
def location():
    location_id = request.args.get("id")
    if location_id is None:
        locations = Location.query.all()

        json = []
        for location in locations:
            json.append({ 
                'id': location.id,
                'name': location.name,
                'description': location.description,
                'occupancy': location.occupancy,
                'capacity': location.capacity,
                })
    else:
        location = Location.query.filter_by(id=location_id).first()
    
        json = { 
            'id': location.id,
            'name': location.name,
            'description': location.description,
            'occupancy': location.occupancy,
            'capacity': location.capacity,
            }

    return jsonify(json)
