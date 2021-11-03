from flask import session, request, redirect, url_for
import requests
import os


def base_url():
    return os.getenv("TMDB_API_URL")

def img_url(path=None, alt=None):
    url = "https://image.tmdb.org/t/p/original"
    if path != None:
        return url + path
    elif alt != None:
        return url + alt
    else:
        return url

def final_url():
    return get_data("/discover/movie?sort_by=popularity.desc&")

def get_data(path):
    api_key = os.getenv("TMDB_API_KEY")
    return (requests.get(f'{base_url()}/{path}api_key={api_key}&language=pt-BR')).json()

def get_data_v4(path):
    url = os.getenv("TMDB_API_URL_v4")
    api_key = os.getenv("TMDB_API_KEY")

    payload = "{}"
    headers = {
        'content-type': "application/json;charset=utf-8",
        'authorization': "Bearer <<access_token>>"
    }

    response = request(
        "GET", f'{url}/{path}api_key={api_key}&language=pt-BR', data=payload, headers=headers)

    return response.text
