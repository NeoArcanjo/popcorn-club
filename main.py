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
    access_token_url=os.getenv("GOOGLE_ACCESS_TOKEN_URL"),
    access_token_params=os.getenv("GOOGLE_ACCESS_TOKEN_PARAMS"),  # None,
    authorize_url=os.getenv("GOOGLE_AUTHORIZE_URL"),
    authorize_params=os.getenv("GOOGLE_AUTHORIZE_PARAMS"), # None,
    api_base_url=os.getenv("GOOGLE_API_BASE_URL"),
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    # os.getenv("GOOGLE_CLIENT_KWARGS")
    client_kwargs={'scope': 'openid email profile'},
)

# spotify = oauth.register(
#     name='spotify',
#     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#     client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     # This is only needed if using openId to fetch user info
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
#     client_kwargs={'scope': 'openid email profile'},
# )

disqus = oauth.register(
    name='disqus',
    client_id=os.getenv("DISQUS_API_KEY"),
    client_secret=os.getenv("DISQUS_API_SECRET"),
    access_token_url=os.getenv("DISQUS_ACCESS_TOKEN"),
    access_token_params={'type': 'code'},
    authorize_url=os.getenv("DISQUS_AUTHORIZE_URL"),
    authorize_params={'type': 'code'},
    api_base_url=os.getenv("DISQUS_API_BASE_URL"),
    client_kwargs={'scope': 'read write'}  ,# os.getenv("DISQUS_CLIENT_KWARGS"),
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
