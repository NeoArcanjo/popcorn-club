# from main import Session

from functions import refreshToken, dbAddTracksPlaylist, dbClearPlaylist, dbGetTopTracksURI
import logging
from sqlalchemy import Column, Index, Integer, String

# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()


# class User(Base):
# 	__tablename__ = 'users'
# 	id = Column(Integer, primary_key=True)
# 	username = Column(String(64))  # , index=True)
# 	refresh_token = Column(String(150))
# 	playlist_id_short = Column(String(30))
# 	playlist_id_medium = Column(String(30))
# 	playlist_id_long = Column(String(30))

# 	# ix_users_username = Index('ix_users_username', username, unique=True)

# 	# refresh_token = Column(String(150), index=True, unique=True)
# 	# playlist_id_short = Column(String(30), index=True, unique=True)
# 	# playlist_id_medium = Column(String(30), index=True, unique=True)
# 	# playlist_id_long = Column(String(30), index=True, unique=True)

# 	def __repr__(self):
# 		return '<User {}>'.format(self.username)


# def addUser(username, refresh_token, playlist_id_short=None, playlist_id_medium=None, playlist_id_long=None):
# 	session = Session()
# 	id_exists = session.query(User.id).filter_by(username=username).scalar()

# 	# new user
# 	if id_exists == None:
# 		user = User(username=username, refresh_token=refresh_token, playlist_id_short=playlist_id_short,
# 		            playlist_id_medium=playlist_id_medium, playlist_id_long=playlist_id_long)
# 		session.add(user)
# 		logging.info('New auto user: ' + username)

# 	#user already exists
# 	else:
# 		user = session.query(User).get(id_exists)
# 		logging.info('Auto user updated: ' + user.username)

# 		# only update playlist IDs that are new
# 		if playlist_id_short != None:
# 			user.playlist_id_short = playlist_id_short
# 		if playlist_id_medium != None:
# 			user.playlist_id_medium = playlist_id_medium
# 		if playlist_id_long != None:
# 			user.playlist_id_long = playlist_id_long

# 	session.commit()
# 	session.close()


def updatePlaylists():
	session = Session()

	# attempt to update each user's playlists
	for user in session.query(User):
		is_active = False

		# authorize the application with Spotify API
		payload = refreshToken(user.refresh_token)

		# if user account has been removed or authorization revoked, user is deleted
		if payload == None:
			session.delete(user)
		else:
			access_token = payload[0]

			playlist = user.playlist_id_short
			if playlist != None:

				# if the playlist has not been deleted
				if (dbClearPlaylist(access_token, playlist) != None):
					uri_list = dbGetTopTracksURI(access_token, 'short_term', 50)
					dbAddTracksPlaylist(access_token, playlist, uri_list)
					is_active = True
				else:
					user.playlist_id_short = None

			playlist = user.playlist_id_medium
			if playlist != None:
				if (dbClearPlaylist(access_token, playlist) != None):
					uri_list = dbGetTopTracksURI(access_token, 'medium_term', 50)
					dbAddTracksPlaylist(access_token, playlist, uri_list)
					is_active = True
				else:
					user.playlist_id_medium = None

			playlist = user.playlist_id_long
			if playlist != None:
				if (dbClearPlaylist(access_token, playlist) != None):
					uri_list = dbGetTopTracksURI(access_token, 'long_term', 50)
					dbAddTracksPlaylist(access_token, playlist, uri_list)
					is_active = True
				else:
					user.playlist_id_long = None

			# if no playlists could be updated, then remove user
			if not is_active:
				session.delete(user)

	session.commit()
	session.close()

	logging.info('Updated TopTracks Playlists')
