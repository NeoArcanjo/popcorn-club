import logging
# import sqlalchemy
import os
from datetime import timedelta
from flask import Flask, redirect, url_for
from flask import render_template
from flask_assets import Environment, Bundle
# from .scheduler import scheduler

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

# dotenv setup
from dotenv import load_dotenv
load_dotenv()
assets = Environment()

def create_app(test_config=None):
    from .auth import auth
    from .dashboard import dashboard
    from .club import club
    from .spotify import spotify
    # from . import routes
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

    # Initialize plugins
    assets.init_app(app)
    # scheduler.start()

    with app.app_context():
        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
        
        app.register_blueprint(auth.bp)
        app.register_blueprint(club.bp)
        app.register_blueprint(dashboard.bp)
        app.register_blueprint(spotify.spotify_bp)
        
        @app.route("/404")
        def e404():
            return render_template('404.html')


        @app.route("/blank")
        def blank():
            return render_template('blank.html')


        @app.route('/')
        def index():
            return redirect(url_for('club.index'))
        
        style_bundle = Bundle(
            'src/less/*.less',
            filters='less,cssmin',
            output='dist/css/style.min.css',
            extra={'rel': 'stylesheet/css'}
        )


        # Register style bundle
        assets.register('main_styles', style_bundle)

        # Build LESS styles
        style_bundle.build()
        return app
