from flask import Flask, render_template, request, url_for
import requests
import random
from functions import get_data, base_url, img_url

app = Flask(__name__)

@app.route('/')
def index():   
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


if __name__ == '__main__':
    app.run()
