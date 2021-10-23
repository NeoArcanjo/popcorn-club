from flask import Flask
import sqlalchemy
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta

# # decorator for routes that should be accessible only by logged in users
# from auth_decorator import login_required

# dotenv setup
from dotenv import load_dotenv
load_dotenv()

# App config
app = Flask(__name__)

# Session config
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
oauth = OAuth(app)

# oAuth Setup
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

engine = sqlalchemy.create_engine(
    os.getenv('SQLALCHEMY_DATABASE_URI'), pool_pre_ping=True)

# # create session and base declarative
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Session = sessionmaker(engine)
# Session = sessionmaker(bind=engine)

insp = sqlalchemy.inspect(engine)  # will be a PGInspector

# make sure user table is created
from models import User
Base.metadata.create_all(engine)

# with Session() as session:
#     session.add(User)
#     session.commit()

import routes
