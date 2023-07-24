from flask import render_template, redirect, request
import base64
import os
import random as rand
import string as string
import requests
import time
import logging


def createStateKey(size):
    # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(rand.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


# def getToken(code):
#     token_url = 'https://accounts.spotify.com/api/token'
#     authorization = str(base64.urlsafe_b64encode(
#         f"{app.config['CLIENT_ID']}:{app.config['CLIENT_SECRET']}".encode('utf-8')), 'utf-8')
#     app.config['AUTHORIZATION'] = authorization
#     redirect_uri = app.config['REDIRECT_URI']
#     headers = {'Authorization': f"basic {authorization}", 'Accept': 'application/json',
#                'Content-Type': 'application/x-www-form-urlencoded'}
#     body = {'code': code, 'redirect_uri': redirect_uri,
#             'grant_type': 'authorization_code'}
#     post_response = requests.post(token_url, headers=headers, data=body)

#     print(post_response)
#     # 200 code indicates access token was properly granted
#     if post_response.status_code == 200:
#         json = post_response.json()
#         return json['access_token'], json['refresh_token'], json['expires_in']
#     else:
#         logging.error('getToken:' + str(post_response.status_code))
#         return None


def refreshToken(refresh_token):
    token_url = 'https://accounts.spotify.com/api/token'
    authorization = app.config['AUTHORIZATION']

    headers = {'Authorization': authorization, 'Accept': 'application/json',
               'Content-Type': 'application/x-www-form-urlencoded'}
    body = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
    post_response = requests.post(token_url, headers=headers, data=body)

    if post_response.status_code == 200:
        return post_response.json()['access_token'], post_response.json()['expires_in']
    logging.error(f'refreshToken:{post_response.status_code}')
    return None


def checkTokenStatus(session):
    if time.time() > session['token_expiration']:
        payload = refreshToken(session['refresh_token'])

        if payload != None:
            session['token'] = payload[0]
            session['token_expiration'] = time.time() + payload[1]
        else:
            logging.error('checkTokenStatus')
            return None

    return "Success"


def makeGetRequest(session, url, params={}):
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, headers=headers, params=params)

    # 200 code indicates request was successful
    if response.status_code == 200:
        return response.json()

    elif response.status_code == 401 and checkTokenStatus(session) != None:
        return makeGetRequest(session, url, params)
    else:
        logging.error(f'makeGetRequest:{response.status_code}')
        return None


def makePutRequest(session, url, params={}, data={}):
    headers = {
        "Authorization": f"Bearer {session['token']}",
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.put(url, headers=headers, params=params, data=data)

    # if request succeeds or specific errors occured, status code is returned
    if response.status_code in {204, 403, 404, 500}:
        return response.status_code

    elif response.status_code == 401 and checkTokenStatus(session) != None:
        return makePutRequest(session, url, data)
    else:
        logging.error(f'makePutRequest:{response.status_code}')
        return None


def makePostRequest(session, url, data):

    headers = {
        "Authorization": f"Bearer {session['token']}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=data)

    # both 201 and 204 indicate success, however only 201 responses have body information
    if response.status_code == 201:
        return response.json()
    if response.status_code == 204:
        return response

    elif response.status_code == 401 and checkTokenStatus(session) != None:
        return makePostRequest(session, url, data)
    elif response.status_code in {403, 404}:
        return response.status_code
    else:
        logging.error(f'makePostRequest:{response.status_code}')
        return None


def makeDeleteRequest(session, url, data):
    headers = {
        "Authorization": f"Bearer {session['token']}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.delete(url, headers=headers, data=data)

    # 200 code indicates request was successful
    if response.status_code == 200:
        return response.json()

    elif response.status_code == 401 and checkTokenStatus(session) != None:
        return makeDeleteRequest(session, url, data)
    else:
        logging.error(f'makeDeleteRequest:{response.status_code}')
        return None


# def getUserInformation(session):
#     url = 'https://api.spotify.com/v1/me'
#     payload = makeGetRequest(session, url)

#     if payload == None:
#         return None

#     return payload


def getAllTopTracks(session, limit=10):
    url = 'https://api.spotify.com/v1/me/top/tracks'
    track_ids = []
    time_range = ['short_term', 'medium_term', 'long_term']

    for time in time_range:
        params = {'limit': limit, 'time_range': time}
        payload = makeGetRequest(session, url, params)

        if payload is None:
            return None

        track_range_ids = [track['id'] for track in payload['items']]
        track_ids.append(track_range_ids)

    return track_ids


def getTopTracksID(session, time, limit=25):
    url = 'https://api.spotify.com/v1/me/top/tracks'
    params = {'limit': limit, 'time_range': time}
    payload = makeGetRequest(session, url, params)

    return None if payload is None else [track['id'] for track in payload['items']]


def getTopTracksURI(session, time, limit=25):
    url = 'https://api.spotify.com/v1/me/top/tracks'
    params = {'limit': limit, 'time_range': time}
    payload = makeGetRequest(session, url, params)

    if payload is None:
        return None

    return [track['uri'] for track in payload['items']]


def getTopArtists(session, time, limit=10):
    url = 'https://api.spotify.com/v1/me/top/artists'
    params = {'limit': limit, 'time_range': time}
    payload = makeGetRequest(session, url, params)

    if payload is None:
        return None

    return [artist['id'] for artist in payload['items']]


def getRecommendedTracks(session, search, tuneable_dict, limit=25):
    track_ids = ""
    artist_ids = ""
    for item in search:

        # tracks IDs start with a 't:' to identify them
        if item[:2] == 't:':
            track_ids += f"{item[2:]},"

        # artist IDs start with an 'a:' to identify them
        if item[:2] == 'a:':
            artist_ids += f"{item[2:]},"

    url = 'https://api.spotify.com/v1/recommendations'
    params = {
        'limit': limit,
        'seed_tracks': track_ids[:-1],
        'seed_artists': artist_ids[:-1],
    }
    params |= tuneable_dict
    payload = makeGetRequest(session, url, params)

    if payload is None:
        return None

    return [track['uri'] for track in payload['tracks']]


def getUserPlaylists(session, limit=20):
    url = 'https://api.spotify.com/v1/me/playlists'
    offset = 0
    playlist = []

    # iterate through all playlists of a user (Spotify limits amount returned with one call)
    total = 1
    while total > offset:
        params = {'limit': limit, 'offset': offset}
        payload = makeGetRequest(session, url, params)

        if payload is None:
            return None

        playlist.extend([item['name'], item['uri']] for item in payload['items'])
        total = payload['total']
        offset += limit

    return playlist


def getUserDevices(session):
    url = 'https://api.spotify.com/v1/me/player/devices'
    payload = makeGetRequest(session, url)

    if payload is None:
        return None

    return [
        [device['name'], device['id']]
        for device in payload['devices']
        if device['is_restricted'] != True
    ]


def startPlayback(session, device):
    url = 'https://api.spotify.com/v1/me/player/play'
    params = {'device_id': device}
    return makePutRequest(session, url, params)


def startPlaybackContext(session, playlist, device):
    url = 'https://api.spotify.com/v1/me/player/play'
    params = {'device_id': device}
    data = "{\"context_uri\":\"" + playlist + \
        "\",\"offset\":{\"position\":0},\"position_ms\":0}"
    return makePutRequest(session, url, params, data)


def pausePlayback(session):
    url = 'https://api.spotify.com/v1/me/player/pause'
    return makePutRequest(session, url)


def shuffle(session, device, is_shuffle=True):
    url = 'https://api.spotify.com/v1/me/player/shuffle'
    params = {'state': is_shuffle, 'device_id': device}
    return makePutRequest(session, url, params)


def skipTrack(session):
    url = 'https://api.spotify.com/v1/me/player/next'
    data = {}
    return makePostRequest(session, url, data)


def getTrack(session):
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    payload = makeGetRequest(session, url)

    if payload is None:
        return None

    # check to make sure the newest track is being grabbed (progress must be under 5000ms)
    if payload['progress_ms'] != None and payload['progress_ms'] > 5000:
        time.sleep(0.2)
        payload = makeGetRequest(session, url)

        if payload is None:
            return None

    name = payload['item']['name']
    img = payload['item']['album']['images'][0]['url']

    return {'name': name, 'img': img}


def getTrackAfterResume(session):
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    payload = makeGetRequest(session, url)

    if payload is None:
        return None

    name = payload['item']['name']
    img = payload['item']['album']['images'][0]['url']

    return {'name': name, 'img': img}


def createPlaylist(session, playlist_name):
    url = 'https://api.spotify.com/v1/users/' + \
        session['user_id'] + '/playlists'
    data = "{\"name\":\"" + playlist_name + \
        "\",\"description\":\"Created by Discover Daily\"}"
    payload = makePostRequest(session, url, data)

    return None if payload is None else (payload['id'], payload['uri'])


def addTracksPlaylist(session, playlist_id, uri_list):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    uri_str = "".join("\"" + uri + "\"," for uri in uri_list)
    data = "{\"uris\": [" + uri_str[:-1] + "]}"
    makePostRequest(session, url, data)

    return


def getTracksPlaylist(session, playlist_id, limit=100):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    offset = 0
    track_uri = []

    # iterate through all tracks in a playlist (Spotify limits number per request)
    total = 1
    while total > offset:
        params = {'limit': limit,
                  'fields': 'total,items(track(uri))', 'offset': offset}
        payload = makeGetRequest(session, url, params)

        if payload is None:
            return None

        track_uri.extend(item['track']['uri'] for item in payload['items'])
        total = payload['total']
        offset += limit

    return track_uri


def searchSpotify(session, search, limit=4):
    url = 'https://api.spotify.com/v1/search'
    params = {'limit': limit, 'q': f"{search}*", 'type': 'artist,track'}
    payload = makeGetRequest(session, url, params)

    if payload is None:
        return None

    results = [
        [item['name'], 'a:' + item['id'], item['popularity']]
        for item in payload['artists']['items']
    ]
    for item in payload['tracks']['items']:

        # track names will include both the name of the track and all artists
        full_name = item['name'] + " - "
        for artist in item['artists']:
            full_name += artist['name'] + ", "

        # append 't:' to track URIs so tracks and artists can be distinguished
        results.append([full_name[:-2], 't:' + item['id'], item['popularity']])

    # sort them by popularity (highest first)
    results.sort(key=lambda x: int(x[2]), reverse=True)

    return [{'label': item[0], 'value': item[1]} for item in results]


def dbAddTracksPlaylist(access_token, playlist_id, uri_list):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    headers = {
        "Authorization": f"Bearer {access_token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    uri_str = "".join("\"" + uri + "\"," for uri in uri_list)
    data = "{\"uris\": [" + uri_str[:-1] + "]}"

    payload = requests.post(url, headers=headers, data=data)

    return "success" if payload.status_code == 201 else None


def dbGetTracksPlaylist(access_token, playlist_id, limit=100):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    headers = {"Authorization": f"Bearer {access_token}"}
    offset = 0
    track_uri = []

    # iterate through all tracks in a playlist (Spotify limits number per request)
    total = 1
    while total > offset:
        params = {'limit': limit,
                  'fields': 'total,items(track(uri))', 'offset': offset}
        payload = requests.get(url, headers=headers, params=params)

        if payload.status_code == 200:
            payload = payload.json()
        else:
            return None

        track_uri.extend(item['track']['uri'] for item in payload['items'])
        total = payload['total']
        offset += limit

    return track_uri


def dbClearPlaylist(access_token, playlist_id):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    uri_list = dbGetTracksPlaylist(access_token, playlist_id)

    uri_str = "".join("{\"uri\":\"" + uri + "\"}," for uri in uri_list)
    data = "{\"tracks\": [" + uri_str[:-1] + "]}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    payload = requests.delete(url, headers=headers, data=data)

    return "success" if payload.status_code == 200 else None


def dbGetTopTracksURI(access_token, time, limit=25):
    url = 'https://api.spotify.com/v1/me/top/tracks'
    params = {'limit': limit, 'time_range': time}
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = requests.get(url, headers=headers, params=params)

    if payload.status_code == 200:
        payload = payload.json()
    else:
        return None

    return [track['uri'] for track in payload['items']]
