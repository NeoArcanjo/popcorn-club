from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from apscheduler.schedulers.background import BackgroundScheduler

import sqlalchemy

# initial app configuration
app = Flask(__name__)
app.config.from_pyfile('config.cfg')

engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True) #, client_encoding="utf8")

# create session and base declarative
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

insp = sqlalchemy.inspect(engine)  # will be a PGInspector

# make sure user table is created
from models import User

Base.metadata.create_all(engine)

# schedule updates for the TopTracks playlists
from models import updatePlaylists

scheduler = BackgroundScheduler()
scheduler.add_job(updatePlaylists, trigger='interval', days=1)
scheduler.start()

import routes
bootstrap = Bootstrap(app)