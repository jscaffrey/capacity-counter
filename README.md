<div align="center">
   <img src="https://raw.githubusercontent.com/jscaffrey/capacity-counter/main/app/static/images/logo-hero.png" alt="" />
</div>

# Capacity Counter
Counter for counting visitors in a physical location. Made with love for libraries monitoring indoor occupancy during the global COVID-19 pandemic.

## Features

### Reduce cognitive load on employees
Free employees to focus on greeting and reminding of health protocols
<div align="center" style="margin: 20px;">
<img src="http://juliacaffrey.com/dist/img/screencapture.gif" alt="Screencapture of Capacity Counter showing the ability to log in, count using large buttons, and reset the number." />
</div>
### Show data on your website using the public API
Give visitors data to inform their decision whether to visit
<div align="center" style="margin: 20px;">
<img src="http://juliacaffrey.com/dist/img/screenshot-occupancy.png" alt="Screencapture of Towson University library website with a section beneath the navigation showing 15 out of 300 visitors" />
</div>
### IoT Device Friendly
If you are using a device for your door count, you can use a GET request to increment "/increment" or decrement "/decrement" as people arrive and depart.

### Add locations, users, and custom links from the command line
####Add a location
<div align="center" style="margin: 20px;">
<img src="https://juliacaffrey.com/dist/img/add-location.gif" alt="Add a location using a command in the terminal"/>
</div>
####Create a user
<div align="center" style="margin: 20px;">
<img src="https://juliacaffrey.com/dist/img/create-user.gif" alt="Create a user using a command in the terminal"/>
</div>
####Add a custom link in your navigation.
### Takes hourly snapshot of current occupancy
Supports data-driven decision making and identifying peak times.

## Stack
Uses Python 3, Flask, and SQLAlchemy. Can be used with MySQL (or MariaDB) or SQLite.

## Usage
In use at Towson University [Albert S. Cook Library](https://libraries.towson.edu)

## Installation
### 1. Install Python3
First install Python3. Check if you have Python installed:

```
$ python3 -V
Python 3.8.2
```

### 2. Install Capacity Counter
Next install the app. You'll need `git` installed. If you need a tutorial to get started, I recommend [this Install Git tutorial by Atlassian/Bitbucket](https://www.atlassian.com/git/tutorials/install-git)
```
git clone https://github.com/jscaffrey/capacity-counter.git
cd capacity-counter
```

### 3. Set up your Flask environment
Enter a virtual environment for Flask.
```
python3 -m venv venv
source venv/bin/activate
```
You should see: `(venv)` appear. If so, ya done good.
If you need more information on this step, see the [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### 4. Install dependencies
All dependencies can be added easily using the following:
```
pip3 install .
```

### 5. Set environmental variables.
Okay, almost there. A few pesky commands away.

Make a copy of the same settings and change it.
```
(venv) $ export FLASK_APP=capacity-counter.py
(venv) $ mv sample-settings.cfg settings.cfg
(venv) $ export CAPACITY_COUNTER=../settings.cfg
```

Next, open `settings.cfg` using your favorite text editor and change the value of `SECRET_KEY` to something secure and long.

### 6. Set up database

#### Option 1: Use SQLite3
Install SQLite3 if you haven't already.

Use the configuration example in `sample-settings.cfg`

#### Option 2: Use MySQL/MariaDB
Install MySQL/MariaDB if you haven't already.

Log in as root.
```
$ mysql -uroot -p
```
Create a database and user for the app. Be sure to store the username and password. You'll need it in the next step.

```
create database capacitycounter character set utf8 collate utf8_bin;
create user 'capacitycounter'@'localhost' identified by 'YOURPASSWORD';
grant all privileges on capacitycounter.* to 'capacitycounter'@localhost';
flush privileges;
quit;
```

In `settings.cfg`, update the database information. This includes the password and user information.
```
SQLALCHEMY_DATABASE_URI = 'mysql+pysql://capacitycounter:YOURPASSWORD@localhost/capacitycounter
```

### 7. Initialize the application

```
python3 -m flask db init
python3 -m flask db migrate
python4 -m flask db upgrade
```

### 8. Serve the application

#### Local environment
For local development / testing, you can use Flask to run the app
```
python3 -m flask run
```

#### Production (live) environment
For running it in production, I suggest gunicorn or an Apache modification. At TU we use [gunicorn](https://pypi.org/project/gunicorn/).

### 9. Add a location

```
python3 -m flask add-location
```
### 10. Make users

```
python3 -m flask create-user
```

## Roadmap
- Status messages when approaching or exceeding capacity
- Users can download a copy a CSV of data over time
- Display web-based reports

## Contribute
Contributions welcome and open to changing to a community open source model for more rapid development if needed.
1. Fork it (<https://github.com/jscaffrey/capacity-counter/fork>)
2. Create your feature branch (`git checkout -b feature/coolThing`)
3. Commit your changes (`git commit -am 'Add some cool thing'`)
4. Push to the branch (`git push origin feature/coolThing`)
5. Create a new Pull Request
