# import routes
# from models import User
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from flask import Flask, render_template
# from flask_bootstrap import Bootstrap

# import sqlalchemy

# # initial app configuration
# app = Flask(__name__)
# app.config.from_pyfile('config.cfg')

# engine = sqlalchemy.create_engine(
#     app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True)  # , client_encoding="utf8")

# # create session and base declarative
# Session = sessionmaker(bind=engine)

# Base = declarative_base()

# insp = sqlalchemy.inspect(engine)  # will be a PGInspector

# # make sure user table is created

# Base.metadata.create_all(engine)

# bootstrap = Bootstrap(app)
import logging
import time
# from .models import addUser
from .functions import refreshToken, checkTokenStatus, getAllTopTracks, getTopTracksID, getTopTracksURI, getTopArtists, getRecommendedTracks, startPlayback, startPlaybackContext, pausePlayback, shuffle, getUserPlaylists, getUserDevices, skipTrack, getTrack, getTrackAfterResume, createPlaylist, addTracksPlaylist, searchSpotify
from flask import Blueprint, render_template, flash, redirect, request, session, make_response, jsonify, abort
from flask import current_app as app, url_for
from popcorn_club.Auth.auth import spotify_required

spotify_bp = Blueprint('spotify_bp', __name__, url_prefix='/soundtracks',
                       template_folder='templates', static_folder='static')


def nav_bar():
    return [{'uri': url_for("spotify_bp.tracks"), 'aria_label': "topTracks", 'name': 'TOPTRACKS'},
            {'uri': url_for("spotify_bp.create"), 'aria_label': "create",
            'name': 'CREATE'},
            {'uri': url_for("spotify_bp.timer"), 'aria_label': "timer", 'name': 'TIMER'}]


@spotify_bp.route('/')
def home():
    return render_template('spotify.html', nav=nav_bar())


"""
Page describes the web applications privacy policy as well as information about
the features provided.
"""


@spotify_bp.route('/information',  methods=['GET'])
def information():
    return render_template('information.html', nav=nav_bar())


"""
TopTracks Feature: This page displays a users TopTracks over several different time
periods.
"""
@spotify_bp.route('/tracks',  methods=['GET'])
@spotify_required
def tracks():
    # collect user information
    if session.get('user_id') == None:
        current_user = session['profile']
        session['user_id'] = current_user['id']

    track_ids = getAllTopTracks(session)

    if track_ids == None:
        return render_template('spotify.html', nav=nav_bar(), error='Failed to gather top tracks.')

    return render_template('tracks.html', track_ids=track_ids)


"""
Create Feature: Page allows users to enter artists/tracks and creates a playlist based
on these entries.
"""
@spotify_bp.route('/create',  methods=['GET'])
@spotify_required
def create():
    # collect user information
    if session.get('user_id') == None:
        current_user = session['profile']
        print(current_user["id"])

        session['user_id'] = current_user['id']

    return render_template('create.html', nav=nav_bar())


"""
Interval Timer Feature: Page displays a form for setting up the timer, which includes
a list of possible playlists to play and devices to play from. It also displays a
countdown timer.
"""
@spotify_bp.route('/timer',  methods=['GET'])
@spotify_required
def timer():
    # TODO: criar um require spotify authorization
    # collect user information
    if session.get('user_id') == None:
        current_user = session['profile']
        session['user_id'] = current_user['id']

    device_names = getUserDevices(session)
    playlist_names = getUserPlaylists(session)

    if device_names == None or playlist_names == None:
        return render_template('spotify.html', nav=nav_bar(), error='Failed to get device ID and playlists.')

    # length is needed to iterate properly with Jinja
    device_length = len(device_names)
    playlist_length = len(playlist_names)

    return render_template('timer.html', playlist_names=playlist_names, playlist_length=playlist_length, device_names=device_names, device_length=device_length)


"""
Called when a user saves a TopTracks playlist. For each playlist that a user saves, a new
playlist is created and filled with TopTracks. If a user selects autoupdate, then the
user and playlist IDs are added to the database so they can be continuously updated.
"""
@spotify_bp.route('/tracks/topplaylist',  methods=['POST'])
def createTopPlaylist():
    # save IDs in case user chose autoupdate
    playlist_id_short = None
    playlist_id_medium = None
    playlist_id_long = None
    playlist_uri = ''

    # create playlist, then get TopTracks, then fill playlist with TopTracks
    if 'short_term' in request.form:
        playlist_id_short, playlist_uri = createPlaylist(
            session, request.form['short_term_name'])
    uri_list = getTopTracksURI(session, 'short_term', 50)
    addTracksPlaylist(session, playlist_id_short, uri_list)

    if 'medium_term' in request.form:
        playlist_id_medium, playlist_uri = createPlaylist(
            session, request.form['medium_term_name'])
    uri_list = getTopTracksURI(session, 'medium_term', 50)
    addTracksPlaylist(session, playlist_id_medium, uri_list)

    if 'long_term' in request.form:
        playlist_id_long, playlist_uri = createPlaylist(
            session, request.form['long_term_name'])
    uri_list = getTopTracksURI(session, 'long_term', 50)
    addTracksPlaylist(session, playlist_id_long, uri_list)

    # # if user selects autoupdate, add them to the database
    # if 'auto_update' in request.form:
    #     addUser(session['user_id'], session['refresh_token'], playlist_id_short=playlist_id_short,
    #             playlist_id_medium=playlist_id_medium, playlist_id_long=playlist_id_long)

    # send back the created playlist URI so the user is redirected to Spotify
    return playlist_uri


"""
Called when a user creates a playlist through the Create feature. All of the user entered
artists/track IDs are gathered from the POST data, as well as any tuneable attributes. Then
create a new playlist, find recommended tracks, and fill the playlist with these tracks.
"""
@spotify_bp.route('/create/playlist',  methods=['POST'])
def createSelectedPlaylist():
    # collect the IDs of the artists/tracks the user entered
    search = []
    for i in range(0, 5):
        if str(i) in request.form:
            search.append(request.form[str(i)])
        else:
            break

    # store all selected attributes in a dict which can be easily added to GET body
    tuneable_dict = {}
    if 'acoustic_level' in request.form:
        tuneable_dict.update({'acoustic': request.form['slider_acoustic']})

    if 'danceability_level' in request.form:
        tuneable_dict.update(
            {'danceability': request.form['slider_danceability']})

    if 'energy_level' in request.form:
        tuneable_dict.update({'energy': request.form['slider_energy']})

    if 'popularity_level' in request.form:
        tuneable_dict.update({'popularity': request.form['slider_popularity']})

    if 'valence_level' in request.form:
        tuneable_dict.update({'valence': request.form['slider_valence']})

    playlist_id, playlist_uri = createPlaylist(
        session, request.form['playlist_name'])
    uri_list = getRecommendedTracks(session, search, tuneable_dict)
    addTracksPlaylist(session, playlist_id, uri_list)

    # send back the created playlist URI so the user is redirected to Spotify
    return playlist_uri


"""
Called when a user starts the Interval Timer feature. The selected playlist and device
are gathered from the POST data. User playback is started with this context.
"""
@spotify_bp.route('/timer/start',  methods=['POST'])
def intervalStart():
    playlist = request.form['playlist']
    session['device'] = request.form['device']

    # toggle shuffle on/off depending on user
    is_shuffle = False
    if 'shuffle' in request.form:
        is_shuffle = True

    response = shuffle(session, session['device'], is_shuffle)

    # if the user does not have a premium account, this feature cannot be used
    if response == 403:
        abort(403)

    # if playback cannot be started on the selected device
    if response == 404:
        abort(404)

    response = startPlaybackContext(session, playlist, session['device'])
    if response == 403:
        abort(403)
    if response == 404:
        abort(404)

    # playback takes a while to start
    time.sleep(0.25)

    # return current track so picture and name can be displayed to user
    current_playing = getTrackAfterResume(session)
    return jsonify(current_playing)


"""
Called when a user starts to enter an artist or track name within the Create feature.
Acts as an endpoint for autocomplete. Takes the entered text and sends back possible
artist or track names.
"""
@spotify_bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    results = searchSpotify(session, search)

    return jsonify(matching_results=results)


"""
Called by front-side JS when an interval is over to skip to next song.
"""
@spotify_bp.route('/playback/skip')
def playbackSkip():
    response = skipTrack(session)

    if response == 403:
        abort(403)
    if response == 404:
        abort(404)

    # return current track so picture and name can be displayed to user
    current_playing = getTrack(session)
    return jsonify(current_playing)


"""
Called by front-side JS when a user pauses the interval timer.
"""
@spotify_bp.route('/playback/pause')
def playbackPause():
    response = pausePlayback(session)

    if response == 403:
        abort(403)
    if response == 404:
        abort(404)
    return "success"


"""
Called by front-side JS when a user resumes a paused interval timer.
"""
@spotify_bp.route('/playback/resume')
def playbackResume():
    response = startPlayback(session, session['device'])

    if response == 403:
        abort(403)
    if response == 404:
        abort(404)

    # return current track so picture and name can be displayed to user
    current_playing = getTrackAfterResume(session)
    return jsonify(current_playing)
