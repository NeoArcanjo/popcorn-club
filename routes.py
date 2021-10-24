from flask import Flask, render_template, request, redirect, url_for, session
import requests
import random
from functions import get_data, base_url, img_url, login_required
from main import app, oauth


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/disqus')
def disqus():
    disqus = oauth.create_client('disqus')  # create the disqus oauth client
    redirect_uri = url_for('authorize', _external=True)
    return disqus.authorize_redirect(redirect_uri)

@app.route('/login/google')
def google():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize_disqus', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/disqus')
def authorize_disqus():
    disqus = oauth.create_client('disqus')  # create the disqus oauth client
    # Access token from google (needed to get user info)
    token = disqus.authorize_access_token()
    # userinfo contains stuff u specificed in the scrope
    resp = disqus.get('userinfo')
    user_info = resp.json()
    user = oauth.disqus.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from disqus
    session['profile'] = user_info
    # make the session permanant so it keeps existing after broweser gets closed
    session.permanent = True
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


@app.route("/search")
@login_required
def search():
    search = request.args.get('q')
    results = get_data(
        f"search/multi?language=en-US&page=1&include_adult=false&query={search}&")
    results = results["results"]
    set_movie = results[0]

    return render_template("search_result.html",  set_movie=set_movie, img_url=img_url, results=results)


@app.route('/')
@login_required
def index():
    popular = get_data(
        'discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&')
    # nacionais = get_data('discover/movie?certification_country=BR&certification.lte=G&sort_by=popularity.desc&')
    popular = popular["results"]
    secure_random = random.SystemRandom()
    set_movie = secure_random.choice(popular)

    trend = get_data('trending/all/week?')
    trend = trend["results"]

    netflix = get_data('discover/tv?with_networks=213&')
    netflix = netflix["results"]

    return render_template('index.html', set_movie=set_movie, img_url=img_url, popular=popular, trend=trend, netflix=netflix)


@app.route('/movie')
@login_required
def movie():
    genres = get_data('genre/movie/list?')
    genres = genres["genres"]

    for genre in genres:
        results = get_data(f'discover/movie?&with_genres={genre["id"]}&')
        genre["results"] = results["results"]

    popular = get_data(
        'discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&')
    popular = popular["results"]
    secure_random = random.SystemRandom()
    set_movie = secure_random.choice(popular)

    trend = get_data('trending/movie/week?')
    trend = trend["results"]

    netflix = get_data('discover/movie?with_networks=213&')
    netflix = netflix["results"]

    return render_template('filmes.html', set_movie=set_movie, img_url=img_url, genres=genres, popular=popular, trend=trend, netflix=netflix)


@app.route('/series')
@login_required
def series():
    genres = get_data('genre/tv/list?')
    genres = genres["genres"]

    for genre in genres:
        results = get_data(f'discover/tv?&with_genres={genre["id"]}&')
        genre["results"] = results["results"]

    popular = get_data(
        'discover/tv?certification_country=US&certification.lte=G&sort_by=popularity.desc&')
    popular = popular["results"]
    secure_random = random.SystemRandom()
    set_show = secure_random.choice(popular)

    # trend = get_data('trending/all/week?')
    trend = get_data('trending/tv/week?')
    trend = trend["results"]

    netflix = get_data('discover/tv?with_networks=213&')
    netflix = netflix["results"]

    return render_template('series.html', set_show=set_show, img_url=img_url, genres=genres, popular=popular, trend=trend, netflix=netflix)


@app.route("/<type>/about/<id>")
@login_required
def about(type, id):
    movie = get_data(f'{type}/{id}?')
    return render_template('sobre.html', movie=movie, img_url=img_url)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html')
