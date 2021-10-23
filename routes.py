from flask import Flask, render_template, request, redirect, url_for, session
import requests
import random
from functions import get_data, base_url, img_url
from main import app

app.secret_key = app.config['SECRET_KEY']

@app.route("/login", methods=["POST", "GET"])
def login():
  # if form is submited
    networks = get_data('networks/list?')
    print(networks)

    if request.method == "POST":
        # record the user name
        session["name"] = request.form.get("name")
        # redirect to the main page
        return redirect("/")
    return render_template("login.html")

@app.route("/search")
def search():
    search = request.args.get('q')
    results = get_data(f"search/multi?language=en-US&page=1&include_adult=false&query={search}&")
    results = results["results"]
    set_movie = results[0]

    return render_template("search_result.html",  set_movie=set_movie, img_url=img_url, results=results)

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/')
def index():
    # check if the users exist or not
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")

    popular = get_data('discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&')
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
def filmes():
    # check if the users exist or not
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")

    genres = get_data('genre/movie/list?')
    genres = genres["genres"]

    for genre in genres:
        results = get_data(f'discover/movie?&with_genres={genre["id"]}&')
        genre["results"] = results["results"]

    popular = get_data('discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&')
    popular = popular["results"]
    secure_random = random.SystemRandom()
    set_movie = secure_random.choice(popular)

    trend = get_data('trending/movie/week?')
    trend = trend["results"]

    netflix = get_data('discover/movie?with_networks=213&')
    netflix = netflix["results"]

    return render_template('filmes.html', set_movie=set_movie, img_url=img_url, genres=genres, popular=popular, trend=trend, netflix=netflix)

@app.route('/series')
def series():
      # check if the users exist or not
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")

    # TODO Guardar api key em arquivo de ambiente
    genres = get_data('genre/tv/list?')
    genres = genres["genres"]

    for genre in genres:
        results = get_data(f'discover/tv?&with_genres={genre["id"]}&')
        genre["results"] = results["results"]

    popular = get_data('discover/tv?certification_country=US&certification.lte=G&sort_by=popularity.desc&')
    popular = popular["results"]
    secure_random = random.SystemRandom()
    set_show = secure_random.choice(popular)

    # trend = get_data('trending/all/week?')
    trend = get_data('trending/tv/week?')
    trend = trend["results"]

    netflix = get_data('discover/tv?with_networks=213&')
    netflix = netflix["results"]

    return render_template('series.html', set_show=set_show, img_url=img_url, genres=genres, popular=popular, trend=trend, netflix=netflix)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html')



