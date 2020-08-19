import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from app import app, db
from app.models import Location, OccupancyOverTime

def commit_occupancy():
    locations = Location.query.all()
    dt = datetime.datetime.now()
    for location in locations:
        o = OccupancyOverTime(occupancy=location.occupancy, datetime=dt,\
                location_id=location.id)
        db.session.add(o)
    
    db.session.commit()

def auto_reset_to_zero():
    locations = Location.query.all()
    dt = datetime.datetime.now()
    for location in locations:
        location.occupancy = 0;

    db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(func=commit_occupancy, trigger="cron", hour="*", minute="25")
scheduler.add_job(func=auto_reset_to_zero, trigger="cron", hour="3", minute="11")
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
