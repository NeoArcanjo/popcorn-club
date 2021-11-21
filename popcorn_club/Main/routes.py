import requests
import random
import json
# from flask import Flask, render_template, request, redirect, url_for, session
from flask import Blueprint, flash, g, render_template, request, url_for
from flask import current_app as app
from werkzeug.exceptions import HTTPException
from base64 import b64encode
from .functions import get_data, img_url
from popcorn_club.Auth.auth import login_required

main_bp = Blueprint('main_bp', __name__, url_prefix='',
               template_folder='templates', static_folder='static')


def nav_bar():
    return [{'uri': url_for("dashboard_bp.dashboard"), 'aria_label': "dashboard", 'name': 'Dashboard'},
            {'uri': "#banner", 'aria_label': "begin", 'name': 'Início'},
            {'uri': url_for("main_bp.tv"),
             'aria_label': "tv", 'name': 'Séries'},
            {'uri': url_for("main_bp.movie"),
             'aria_label': "movies", 'name': 'Filmes'},
            {'uri': "#trends", 'aria_label': "trends", 'name': 'Bombando'},
            {'uri': "#mylist", 'aria_label': "mylist", 'name': 'Minha lista'},
            {'uri': url_for("spotify_bp.home"), 'aria_label': "soundtrack", 'name': 'SoundTrack'}]

@main_bp.route("/search")
@login_required
def search():
    search = request.args.get('q')
    results = get_data(
        f"search/multi?language=en-US&page=1&include_adult=false&query={search}&")
    results = results["results"]
    set_movie = results[0]
    return render_template("search_result.html", set_movie=set_movie, img_url=img_url, results=results, nav=nav_bar())


@main_bp.route('/')
@main_bp.route('/index')
@main_bp.route('/home')
@login_required
def index():
    with open('tmp/json/popular.json', 'r') as f:
        popular = json.load(f)

    with open('tmp/json/trend.json', 'r') as f:
        trend = json.load(f)

    with open('tmp/json/netflix.json', 'r') as f:
        netflix = json.load(f)

    secure_random = random.SystemRandom()
    set_movie = secure_random.choice(popular)

    return render_template('index.html', set_movie=set_movie, img_url=img_url, popular=popular, trend=trend, netflix=netflix, nav=nav_bar())


@main_bp.route('/movie')
@login_required
def movie():
    with open('tmp/json/movie/genres.json', 'r') as f:
        genres = json.load(f)
    genres = genres["genres"]

    for genre in genres:
        with open(f'tmp/json/movie/{genre["name"]}.json', 'r') as f:
            genre["results"] = json.load(f)

    with open('tmp/json/movie/popular.json', 'r') as f:
        popular = json.load(f)

    with open('tmp/json/movie/trend.json', 'r') as f:
        trend = json.load(f)

    with open('tmp/json/movie/netflix.json', 'r') as f:
        netflix = json.load(f)

    secure_random = random.SystemRandom()
    set_movie = secure_random.choice(popular)

    return render_template('filmes.html', set_movie=set_movie, img_url=img_url, genres=genres, popular=popular, trend=trend, netflix=netflix, nav=nav_bar())


@main_bp.route('/tv')
@login_required
def tv():
    with open('tmp/json/tv/genres.json', 'r') as f:
        genres = json.load(f)
    genres = genres["genres"]

    for genre in genres:
        with open(f'tmp/json/tv/{genre["name"]}.json', 'r') as f:
            genre["results"] = json.load(f)

    with open('tmp/json/tv/popular.json', 'r') as f:
        popular = json.load(f)

    with open('tmp/json/tv/trend.json', 'r') as f:
        trend = json.load(f)

    with open('tmp/json/tv/netflix.json', 'r') as f:
        netflix = json.load(f)

    secure_random = random.SystemRandom()
    set_show = secure_random.choice(popular)

    return render_template('series.html', set_show=set_show, img_url=img_url, genres=genres, popular=popular, trend=trend, netflix=netflix, nav=nav_bar())


@main_bp.route("/<type>/about/<id>")
# @login_required
def about(type, id):
    movie = get_data(f'{type}/{id}?')
    aprovacao = ""
    if "vote_average" in movie:
        if movie["vote_average"] >= 8:
            aprovacao = "badge-success"
        elif movie["vote_average"] >= 6:
            aprovacao = "badge-warning"
        else:
            aprovacao = "badge-danger"
    return render_template('sobre.html', movie=movie, img_url=img_url, aprovacao=aprovacao, nav=nav_bar())


@main_bp.errorhandler(HTTPException)
def handle_exception(e):
    code = e.code
    resp = requests.get(f"http://http.cat/{code}")
    obj = resp.content
    image = b64encode(obj).decode("utf-8")
    return render_template("error_generic.html", title=e.name, description=e.description, image=image, code=code, nav=nav_bar()), code
