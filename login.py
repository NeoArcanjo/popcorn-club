from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.exceptions import HTTPException
import requests
import random
import os
from functions import get_data, base_url, img_url, login_required
from base64 import b64encode
from main import app, oauth


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/disqus')
def disqus():
    disqus = oauth.create_client('disqus')  # create the disqus oauth client
    redirect_uri = url_for('authorize_disqus', _external=True)
    print(redirect_uri)
    return disqus.authorize_redirect(redirect_uri)


@app.route('/login/google')
def google():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/spotify')
def spotify():
    spotify = oauth.create_client('spotify')  # create the spotify oauth client
    redirect_uri = url_for('authorize_spotify', _external=True)
    return spotify.authorize_redirect(redirect_uri)


@app.route('/disqus/callback')
def authorize_disqus():
    disqus = oauth.create_client('disqus')  # create the disqus oauth client
    # Access token from disqus (needed to get user info)
    token = disqus.authorize_access_token(client_id=disqus.client_id,
                                          client_secret=disqus.client_secret)
    # userinfo contains stuff u specificed in the scrope
    print(token)
    user_id = token['user_id']
    resp = disqus.userinfo()
    print(resp)
    # user_info = resp.json()
    user_info = {'username': token['username'], 'given_name': token['username'],
                 'picture': f'https://disqus.com/api/users/avatars/{token["username"]}.jpg'}
    print(f'https://disqus.com/api/users/avatars/{token["username"]}.jpg')
    # user = oauth.disqus.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from disqus
    session['profile'] = user_info
    # make the session permanant so it keeps existing after broweser gets closed
    session.permanent = False
    return redirect('/')


@app.route('/spotify/callback')
def authorize_spotify():
    spotify = oauth.create_client('spotify')  # create the spotify oauth client
    # Access token from spotify (needed to get user info)
    token = spotify.authorize_access_token()
    # userinfo contains stuff u specificed in the scrope
    user = oauth.spotify.userinfo()

    user_info = {'username': user['display_name'],
                 'given_name': user['display_name'], 'picture': user['images'][0]['url']}
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from spotify
    session['profile'] = user_info
    # make the session permanant so it keeps existing after broweser gets closed
    session.permanent = False
    return redirect('/')


@app.route('/login/callback')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    # Access token from google (needed to get user info)
    token = google.authorize_access_token()
    # userinfo contains stuff u specificed in the scrope
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    # make the session permanant so it keeps existing after broweser gets closed
    session.permanent = True
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')
