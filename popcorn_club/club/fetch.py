from .functions import get_data
import os
import json

def maybe_create(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return True

def get_genres():
    movie = get_data('genre/movie/list?')
    tv = get_data('genre/tv/list?')

    for name, data in {"movie": movie, "tv": tv}.items():
        path = f'static/tmp/json/{name}'
        maybe_create(path)
        with open(f'{path}/genres.tmp.json', 'w') as f:
            f.write(json.dumps(data))

        os.rename(f'{path}/genres.tmp.json', f'{path}/genres.json')


def get_outliers():
    path = f'static/tmp/json'
    maybe_create(path)
    popular = get_data(
        'discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&')

    popular = popular["results"]

    nacionais = get_data(
        'discover/movie?certification_country=BR&certification.lte=G&sort_by=popularity.desc&')
    nacionais = nacionais["results"]

    trend = get_data('trending/all/week?')
    trend = trend["results"]

    netflix = get_data('discover/tv?with_networks=213&')
    netflix = netflix["results"]

    for name, data in {"nacionais": nacionais, "popular": popular, "trend": trend, "netflix": netflix}.items():
        with open(f'{path}/{name}.tmp.json', 'w') as f:
            f.write(json.dumps(data))

        os.rename(f'{path}/{name}.tmp.json', f'{path}/{name}.json')
    return True


def get_movie():
    path = f'static/tmp/json/movie/'
    maybe_create(path)

    with open(f'static/tmp/json/movie/genres.json', 'r') as f:
        genres = json.load(f)
    genres = genres["genres"]

    for genre in genres:
        results = get_data(f'discover/movie?&with_genres={genre["id"]}&')
        genre["results"] = results["results"]
        with open(f'{path}/{genre["name"]}.tmp.json', 'w') as f:
            f.write(json.dumps(genre["results"]))

        os.rename(f'{path}/{genre["name"]}.tmp.json',
                  f'{path}/{genre["name"]}.json')

    popular = get_data(
        'discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&')
    popular = popular["results"]

    nacionais = get_data(
        'discover/movie?certification_country=BR&certification.lte=G&sort_by=popularity.desc&')
    nacionais = nacionais["results"]

    trend = get_data('trending/movie/week?')
    trend = trend["results"]

    netflix = get_data('discover/movie?with_networks=213&')
    netflix = netflix["results"]

    for name, data in {"nacionais": nacionais, "popular": popular, "trend": trend, "netflix": netflix}.items():
        with open(f'{path}/{name}.tmp.json', 'w') as f:
            f.write(json.dumps(data))

        os.rename(f'{path}/{name}.tmp.json', f'{path}/{name}.json')
    return True


def get_tv():
    path = f'static/tmp/json/tv'
    maybe_create(path)
    with open(f'static/tmp/json/tv/genres.json', 'r') as f:
        genres = json.load(f)
    genres = genres["genres"]

    for genre in genres:
        results = get_data(f'discover/tv?&with_genres={genre["id"]}&')
        genre["results"] = results["results"]

        with open(f'{path}/{genre["name"]}.tmp.json', 'w') as f:
            f.write(json.dumps(genre["results"]))

        os.rename(f'{path}/{genre["name"]}.tmp.json',
                  f'{path}/{genre["name"]}.json')

    popular = get_data(
        'discover/tv?certification_country=US&certification.lte=G&sort_by=popularity.desc&')
    popular = popular["results"]

    nacionais = get_data(
        'discover/tv?certification_country=BR&certification.lte=G&sort_by=popularity.desc&')
    nacionais = nacionais["results"]

    trend = get_data('trending/tv/week?')
    trend = trend["results"]

    netflix = get_data('discover/tv?with_networks=213&')
    netflix = netflix["results"]

    for name, data in {"nacionais": nacionais, "popular": popular, "trend": trend, "netflix": netflix}.items():
        with open(f'{path}/{name}.tmp.json', 'w') as f:
            f.write(json.dumps(data))

        os.rename(f'{path}/{name}.tmp.json',
                  f'{path}/{name}.json')

    return True


def updateMedialists():
    print("Rodando Tarefa...")
    print("Obtendo gêneros...")
    get_genres()
    print("Obtendo destaques...")
    get_outliers()
    print("Obtendo filmes...")
    get_movie()
    print("Obtendo séries...")
    get_tv()
