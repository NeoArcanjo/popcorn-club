# import os
# import logging
# # import scheduler
# import sqlalchemy
# from authlib.integrations.flask_client import OAuth
# import os
# from dotenv import load_dotenv

# # dotenv setup
# load_dotenv()

# # print(app)
# oauth = OAuth(app)
# print(oauth)

# # oAuth Setup
# google = oauth.register(
#     name='google',
#     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#     client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
#     access_token_url=os.getenv("GOOGLE_ACCESS_TOKEN_URL"),
#     access_token_params=os.getenv("GOOGLE_ACCESS_TOKEN_PARAMS"),  # None,
#     authorize_url=os.getenv("GOOGLE_AUTHORIZE_URL"),
#     authorize_params=os.getenv("GOOGLE_AUTHORIZE_PARAMS"),  # None,
#     api_base_url=os.getenv("GOOGLE_API_BASE_URL"),
#     # This is only needed if using openId to fetch user info
#     userinfo_endpoint=os.getenv('GOOGLE_USER_INFO_URL'),
#     # os.getenv("GOOGLE_CLIENT_KWARGS")
#     client_kwargs={'scope': 'openid email profile'},
# )

# # oAuth Setup
# facebook = oauth.register(
#     name='facebook',
#     client_id=os.getenv("FACEBOOK_CLIENT_ID"),
#     client_secret=os.getenv("FACEBOOK_CLIENT_SECRET"),
#     access_token_url=os.getenv("FACEBOOK_ACCESS_TOKEN_URL"),
#     access_token_params=os.getenv("FACEBOOK_ACCESS_TOKEN_PARAMS"),  # None,
#     authorize_url=os.getenv("FACEBOOK_AUTHORIZE_URL"),
#     authorize_params=os.getenv("FACEBOOK_AUTHORIZE_PARAMS"),  # None,
#     api_base_url=os.getenv("FACEBOOK_API_BASE_URL"),
#     # This is only needed if using openId to fetch user info
#     userinfo_endpoint=os.getenv('FACEBOOK_USER_INFO_URL'),
#     # os.getenv("FACEBOOK_CLIENT_KWARGS")
#     client_kwargs={'scope': 'openid email profile'},
# )

# spotify = oauth.register(
#     name='spotify',
#     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
#     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
#     access_token_url=os.getenv("SPOTIFY_ACCESS_TOKEN_URL"),
#     access_token_params={'type': 'code'},
#     authorize_url=os.getenv("SPOTIFY_AUTHORIZE_URL"),
#     authorize_params={'grant_type': 'authorization_code'},
#     api_base_url=os.getenv("SPOTIFY_API_BASE_URL"),
#     # This is only needed if using openId to fetch user info
#     userinfo_endpoint=os.getenv('SPOTIFY_USER_INFO_URL'),
#     # os.getenv("SPOTIFY_CLIENT_KWARGS")
#     client_kwargs={'scope': 'user-read-private user-read-email'},
# )

# disqus = oauth.register(
#     name='disqus',
#     api_key=os.getenv("DISQUS_CLIENT_ID"),
#     api_secret=os.getenv("DISQUS_CLIENT_SECRET"),
#     client_id=os.getenv("DISQUS_CLIENT_ID"),
#     client_secret=os.getenv("DISQUS_CLIENT_SECRET"),
#     access_token_url=os.getenv("DISQUS_ACCESS_TOKEN_URL"),
#     access_token_params={'type': 'code'},
#     authorize_url=os.getenv("DISQUS_AUTHORIZE_URL"),
#     authorize_params={'grant_type': 'authorization_code'},
#     api_base_url=os.getenv("DISQUS_API_BASE_URL"),
#     userinfo_endpoint=os.getenv("DISQUS_USER_INFO_URL"),
#     # os.getenv("DISQUS_CLIENT_KWARGS"),
#     client_kwargs={'scope': "read,write"},
# )

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
