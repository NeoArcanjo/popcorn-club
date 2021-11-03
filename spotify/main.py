import routes
from models import updatePlaylists
from models import User
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from apscheduler.schedulers.background import BackgroundScheduler

import sqlalchemy

# initial app configuration
app = Flask(__name__)
app.config.from_pyfile('config.cfg')

engine = sqlalchemy.create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True)  # , client_encoding="utf8")

# create session and base declarative
Session = sessionmaker(bind=engine)

Base = declarative_base()

insp = sqlalchemy.inspect(engine)  # will be a PGInspector

# make sure user table is created

Base.metadata.create_all(engine)

# schedule updates for the TopTracks playlists

scheduler = BackgroundScheduler()
scheduler.add_job(updatePlaylists, trigger='interval', days=1)
scheduler.start()

bootstrap = Bootstrap(app)
