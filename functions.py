import requests

def img_url():
    return "https://image.tmdb.org/t/p/original"
    
def base_url():
    return "https://api.themoviedb.org/3"

def img_url():
    return "https://image.tmdb.org/t/p/original"

def img_url(path, alt = ""):
    print(path)
    print(alt)
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
    # TODO Guardar api key em arquivo de ambiente
    api = "api_key=f4066aad057be2997b4bc0043b3a4869"
    print(f'{base_url()}/{path}{api}&language=pt-BR')
    return (requests.get(f'{base_url()}/{path}{api}&language=pt-BR')).json()

def get_data_v4(path):
    url = "https://api.themoviedb.org/4"
    # TODO Guardar api key em arquivo de ambiente
    api = "api_key=f4066aad057be2997b4bc0043b3a4869"

    payload = "{}"
    headers = {
        'content-type': "application/json;charset=utf-8",
        'authorization': "Bearer <<access_token>>"
    }

    response = request("GET", f'{url}/{path}{api}&language=pt-BR', data = payload, headers = headers)

    return response.text
