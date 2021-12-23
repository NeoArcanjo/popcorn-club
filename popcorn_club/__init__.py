import logging
import sqlalchemy
import os
from datetime import timedelta
from flask import Flask, redirect, url_for, render_template
from flask_assets import Environment
from popcorn_club.util_assets import bundles

def compile_static_assets(app, assets):
    """Create stylesheet bundles."""
    assets.auto_build = True
    assets.debug = True

    assets.register(bundles)
    # if app.config['ENV'] == 'development':
    #     for bundle in bundles.values():
    #         bundle.build()
    return assets

# dotenv setup
from dotenv import load_dotenv
load_dotenv()
assets = Environment()

def create_app(test_config=None):
    from .Admin import admin
    from .Auth import auth
    from .Main import routes
    from .Dashboard import dashboard
    from .Documentation import documentation
    from .Landing import landing
    from .Spotify import spotify

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Session config
    app.config.from_mapping(
        FLASK_ENV='development',
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

    with app.app_context():
        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        app.register_blueprint(admin.admin_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(dashboard.dashboard_bp)
        app.register_blueprint(documentation.documentation_bp)
        app.register_blueprint(landing.landing_bp)
        app.register_blueprint(spotify.spotify_bp)

        @app.route("/404")
        def e404():
            return render_template('404.html')

        @app.route("/blank")
        def blank():
            return render_template('blank.html')

        @app.route('/')
        def index():
            return redirect(url_for('main_bp.index'))

        # Compile static assets
        compile_static_assets(app, assets)  # Execute logic

        return app


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
