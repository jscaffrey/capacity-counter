#Home page route
import datetime
from flask import render_template, request, jsonify, url_for,\
        redirect, flash, render_template_string
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.models import User, Location, OccupancyOverTime, Links, UserSettings
from app.forms import LoginForm

@app.route('/')
def index():
    location_id = request.args.get("id", 1)
    location = Location.query.filter_by(id=location_id).first()
    links = Links.query.order_by(Links.weight).all()
    rendered_links = []
    for link in links:
        url = render_template_string(link.url, now=datetime.datetime.now())
        rendered_links.append((link.label, url))
    return render_template('index.html', title='Home', location=location, \
        links=rendered_links)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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

@app.route('/reset')
def reset():
    location_id = request.args.get("id", 1)
    location = Location.query.filter_by(id=location_id).first()
    
    location.occupancy = 0
    
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/location')
def location():
    location_id = request.args.get("id")
    if location_id is None:
        locations = Location.query.all()

        json = []
        for location in locations:
            percentage_raw = location.occupancy / location.capacity * 100
            json.append({ 
                'id': location.id,
                'name': location.name,
                'description': location.description,
                'occupancy': location.occupancy,
                'capacity': location.capacity,
                'percentage': round( percentage_raw, 0 )
                })
    else:
        location = Location.query.filter_by(id=location_id).first()

        percentage_raw = location.occupancy / location.capacity * 100
        json = { 
            'id': location.id,
            'name': location.name,
            'description': location.description,
            'occupancy': location.occupancy,
            'capacity': location.capacity,
            'percentage': round( percentage_raw, 0 )
            }

    return jsonify(json)
