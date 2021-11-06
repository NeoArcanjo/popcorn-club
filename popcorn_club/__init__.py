# import os
# import logging
# # import scheduler
# import sqlalchemy
# from authlib.integrations.flask_client import OAuth
# import os
# from dotenv import load_dotenv

# # dotenv setup
# load_dotenv()
import os
from datetime import timedelta
from flask import Flask
# from scheduler import scheduler
import time
# from club.fetch import get_genres, get_outliers, get_movie, get_tv

# # # engine = sqlalchemy.create_engine(
# # #     os.getenv('DATABASE_URL'), pool_pre_ping=True)

# # # logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)

# # # # create session and base declarative
# # # from sqlalchemy.orm import sessionmaker

# # # from sqlalchemy.ext.declarative import declarative_base
# # # Base = declarative_base()
# # # Session = sessionmaker(engine)
# # # Session = sessionmaker(bind=engine)

# # # insp = sqlalchemy.inspect(engine)  # will be a PGInspector

# # # # make sure user table is created
# # # from models import User
# # # Base.metadata.create_all(engine)

# # # with Session() as session:
# # #     session.add(User)
# # #     session.commit()
def create_app(test_config=None):
    from popcorn_club.auth import auth
    from popcorn_club.dashboard import dashboard
    from popcorn_club.club import club
    # from popcorn_club.spotify import spotify
    
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Session config
    app.config.from_mapping(
        SECRET_KEY=os.getenv("APP_SECRET_KEY"),
        SESSION_COOKIE_NAME='google-login-session',
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=5),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.cfg', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(club.bp)
    app.register_blueprint(dashboard.bp)
    # app.register_blueprint(spotify.bp)
    
    # scheduler.start()

    return app
