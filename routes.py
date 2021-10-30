from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.exceptions import HTTPException
import requests
import random
import os
from functions import get_data, base_url, img_url, login_required
from base64 import b64encode
from main import app, oauth
import dashboard
import login

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
@app.route('/index')
@app.route('/home')
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

@app.route('/filmes')
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
@app.route('/tv')
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


@app.errorhandler(HTTPException)
def handle_exception(e):
    code = e.code
    resp = requests.get(f"http://http.cat/{code}")
    obj = resp.content
    image = b64encode(obj).decode("utf-8")
    return render_template("error_generic.html", title=e.name, description=e.description, image=image, code=code), code

# @app.errorhandler(404)
# def page_not_found(e):
#     print(e)
#     resp = requests.get("http://http.cat/404")
#     obj = resp.content
#     image = b64encode(obj).decode("utf-8")
#     return render_template('not_found.html', obj=obj, image=image), 404
