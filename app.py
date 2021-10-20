from flask import Flask, render_template, request, url_for
import requests
import random

app = Flask(__name__)

@app.route('/')
def index():
    # TODO Guardar api key em arquivo de ambiente
    api = "api_key=f4066aad057be2997b4bc0043b3a4869"
    base_url = "https://api.themoviedb.org/3"
    final_url = base_url + "/discover/movie?sort_by=popularity.desc&" + api
    img_url = "https://image.tmdb.org/t/p/original"

    genres = requests.get(f'{base_url}/genre/movie/list?{api}&language=pt-BR')
    genres = genres.json()["genres"]

    for genre in genres:
        results = requests.get(f'{base_url}/discover/movie?{api}&with_genres={genre["id"]}&language=pt-BR')
        results =  results.json()["results"]
        genre["results"] = results

    print(genres[0])

    fetchPopular = requests.get(
        f'{base_url}/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&{api}&language=pt-BR')
    fetchTrending = requests.get(
        f'{base_url}/trending/all/week?{api}&language=pt-BR')
    fetchNetflixOriginals = requests.get(
        f'{base_url}/discover/tv?{api}&with_networks=213&language=pt-BR')
    
    popular = fetchPopular.json()
    popular = popular["results"]
    secure_random = random.SystemRandom()
    set_movie = secure_random.choice(popular)

    trend = fetchTrending.json()
    trend = trend["results"]

    netflix = fetchNetflixOriginals.json()
    netflix = netflix["results"]

    return render_template('index.html', set_movie=set_movie, img_url=img_url, genres=genres, popular=popular, trend=trend, netflix=netflix)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html')


if __name__ == '__main__':
    app.run()
