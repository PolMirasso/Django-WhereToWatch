from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup as bs
from django.http import JsonResponse
import json
import environ
from pathlib import Path
import os
import urllib.parse

BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)


# Scrapping


def getFilmDataCinema(request):
    if request.method == 'POST':


        film_name = request.POST['film_name']
        # film_date = request.POST['film_date']

        searchUrl = os.environ.get('Scraping_URL')+"/ajax/_buscar/"

        form_data = {'queryString': film_name}

        search_r = requests.post(searchUrl,data=form_data)
        search_soup = bs(search_r.content, features="html.parser")

        h2_pelis = search_soup.find('h2', text='Películas')
        film_url = h2_pelis.find_next_sibling('a')['href']
     
        film_url += "cartelera/"
        # +film_date+"/"


        r = requests.get(film_url)
        soup = bs(r.content, features="html.parser")

        ul_element = soup.find('ul', {'class': 'cart-nav'})

        film_id_poster = soup.find('img', {'height': '513'})['src']
        film_id_poster = film_id_poster.split(os.environ.get('Scraping_URL')+'/carteles/fondos/')[1]
        film_id_poster = film_id_poster.split('/')[1]
        film_id = film_id_poster.split('-')[0]

        datos_dict = {}
        for a_element in soup.select('li > a.prov'):
            prov_nombre = a_element.text
            ciudad_dict = {}
            ul_element = a_element.find_next_sibling('ul')
            if ul_element:
                for li_element in ul_element.select('li.c-cartelera'):
                    ciudad_id = li_element['data-id']
                    ciudad_nombre = li_element.text.strip()
                    ciudad_dict[ciudad_id] = ciudad_nombre
            datos_dict[prov_nombre] = ciudad_dict


        datos_dict['film_id'] = film_id


        json_obj = json.dumps(datos_dict, ensure_ascii=False)

        return HttpResponse(json_obj)


def getCinemaData(request):

    if request.method == 'POST':
        
        film_id = request.POST['film_id']
        idprov = request.POST['idprov']
        date = request.POST['date']

        url = env('Scraping_URL')+"/ajax/_cargar_cines/"
        form_data = {'id': idprov, 'fecha': date, 'idp': film_id}

        r = requests.post(url, data=form_data)

        soup = bs(r.content, features="html.parser")


        div_elements = soup.find_all('div', {'class': 'citem'})

        datos_list = []
        for div_element in div_elements:
            cine = div_element.find('span', {'class': 'name'}).text
            horas_span = div_element.find_all('span', {'class': ['time', 'buy']})
            horas = []
            for hora_span in horas_span:
                horas.append(hora_span.text)
            if len(horas) == 1:
                datos_list.append({'cine': cine, 'hora': horas[0]})
            else:
                datos_list.append({'cine': cine, 'hora': horas[:-1]})


        json_obj = json.dumps(datos_list, ensure_ascii=False)

        return HttpResponse(json_obj)

      

def getAllData(request):


    url = env('Scraping_URL')+"peliculas/creed-3/cartelera/20230308/"

    r = requests.get(url)
    soup = bs(r.content, features="html.parser")
    idpelicula = soup.find('div', {'id': 'showtimes'})['rel']


    codis_ubis = [span['rel'] for span in soup.findAll('span', {'class': 'stprov'})]
    nom_ubi = [span.find('h3').text for span in soup.findAll('span', {'class': 'stprov'})]


    dades_pelicules = []

    for i in range(len(codis_ubis)):

        dades_pelicules.append(nom_ubi[i])


        url2 = env('Scraping_URL')+"controlador/films/_filmlistingscities.php?idprov="+codis_ubis[i]+"&fecha=2023-03-08&idpeli="+idpelicula
        
        print("url: "+ url2)
        
        r2 = requests.get(url2)
        soup2 = bs(r2.content, features="html.parser")

        nom_provincies = [span.find('h4').text for span in soup2.findAll('span', {'class': 'stcity'})]
        
        nom_provincies_filtered = [s.split(' (')[0] for s in nom_provincies]

        idcity = [span['rel'] for span in soup2.findAll('span', {'class': 'stcity'})]


        for j in range(len(nom_provincies_filtered)):



            url3 = env('Scraping_URL')+"/controlador/films/_filmlistingscinemas.php?idcity="+idcity[j]+"&fecha=2023-03-08&idpeli="+idpelicula

            print("url3: "+ url3)

            r3 = requests.get(url3)
            soup3 = bs(r3.content, features="html.parser")


            div_infocine = [div for div in soup3.findAll('div', {'class': 'wrapshowtimes'})]

            values_array = [nom_provincies_filtered[j]]

            for div in div_infocine:
                values = div.text.strip().split('\n\n\n\n')

                values_hours = []

                for v in values:
                    mod_hours = v.replace('\n\n\n',',')
                    mod_hours = mod_hours.replace('\n','')

                    values_hours.append(mod_hours)

                values_array.append(values_hours)

            dades_pelicules.append(values_array)


    json_list = list(dades_pelicules)   
    return JsonResponse(json_list,safe=False,json_dumps_params={'ensure_ascii':False})

#API Manager

def getTopRatedFilms(request):

    if request.method == 'POST':


        num_page = request.POST['num_page']
        language = request.POST['language']

        print(num_page)
        print(language)

        url = env("API_URL")+"/3/movie/top_rated?api_key="+env('API_KEY')+"&language="+language+"&page="+num_page+"&region="+language

        headers = {'Accept': 'application/json'}

        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
            movies = [{"film_id": movie["id"], "title": movie["title"], "vote_average": movie["vote_average"], "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/"+movie["poster_path"]} for movie in api["results"]]
            api = movies
        except Exception as e:
            api = {"error": str(e)}
            
        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})


def getPopularFilms(request):

    if request.method == 'POST':

        num_page = request.POST['num_page']
        language = request.POST['language']

        print(language)

        url = env("API_URL")+"/3/movie/popular?api_key="+env('API_KEY')+"&language="+language+"&page="+num_page

        headers = {'Accept': 'application/json'}

        api_requests = requests.get(url, headers=headers)



        try:
            api = json.loads(api_requests.content)
            movies = [{"film_id": movie["id"], "title": movie["title"], "vote_average": movie["vote_average"], "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/"+movie["poster_path"]} for movie in api["results"]]
            api = movies
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})

def getUpcomingFilms(request):

    if request.method == 'POST':

        num_page = request.POST['num_page']
        language = request.POST['language']

        print(language)

        url = env("API_URL")+"/3/movie/upcoming?api_key="+env('API_KEY')+"&language="+language+"&page="+num_page+"&region="+language

        headers = {'Accept': 'application/json'}

        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
            movies = [{"film_id": movie["id"], "title": movie["title"], "vote_average": movie["vote_average"],"genre_ids": movie["genre_ids"], "release_date": movie["release_date"],  
                    "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+movie["poster_path"],
                    "backdrop_path": "https://image.tmdb.org/t/p/w1920_and_h800_multi_faces"+str(movie["backdrop_path"])} 
                    for index, movie in enumerate(api["results"]) if index < 5 and movie["backdrop_path"] is not None]
            api = movies
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})


def getFilmData(request):

    if request.method == 'POST':

        movie_id = request.POST['movie_id']
        language = request.POST['language']

        url = env("API_URL")+"/3/movie/"+movie_id+"?api_key="+env('API_KEY')+"&language="+language

        headers = {'Accept': 'application/json'}

        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})
    

def getSimilarMovie(request):

    if request.method == 'POST':

        movie_id = request.POST['movie_id']
        language = request.POST['language']
        page_num = request.POST['page_num']

        url = env("API_URL")+"/3/movie/"+movie_id+"/similar?api_key="+env('API_KEY')+"&language="+language+"&page="+page_num
        headers = {'Accept': 'application/json'}

        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
            movies = [{"film_id": movie["id"], "title": movie["title"], "vote_average": movie["vote_average"],"genre_ids": movie["genre_ids"], "release_date": movie["release_date"],  
                    "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+movie["poster_path"],
                    "backdrop_path": "https://image.tmdb.org/t/p/w1920_and_h800_multi_faces"+str(movie["backdrop_path"])} 
                    for index, movie in enumerate(api["results"]) if index < 5 and movie["backdrop_path"] is not None]
            api = movies
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})
    

def getProviders(request):

    if request.method == 'POST':

        movie_id = request.POST['movie_id']
        language = request.POST['language']

        url = env("API_URL")+"/3/movie/"+movie_id+"/watch/providers?api_key="+env('API_KEY')+"&language="+language

        print(url)

        headers = {'Accept': 'application/json'}

        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)           
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})


def getAlternativeTitles(request):

    if request.method == 'POST':

        movie_id = request.POST['movie_id']
      
        url = env("API_URL")+"/3/movie/"+movie_id+"/alternative_titles?api_key="+env('API_KEY')

        headers = {'Accept': 'application/json'}

        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})
    
def getMovieRecommendations(request):

    if request.method == 'POST':

        movie_id = request.POST['movie_id']
        page = request.POST['num_page']
        language = request.POST['language']

        url = env("API_URL")+"/3/movie/"+movie_id+"/recommendations?api_key="+env('API_KEY')+"&language="+language+"&page="+page
        headers = {'Accept': 'application/json'}

        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})
    

def getMovieVideos(request):

    if request.method == 'POST':

        movie_id = request.POST['movie_id']
        language = request.POST['language']

        url = env("API_URL")+"/3/movie/"+movie_id+"/videos?api_key="+env('API_KEY')+"&language="+language
        headers = {'Accept': 'application/json'}

        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
            movies = [{"id": movie["id"], "name": movie["name"], "video": "https://youtu.be/"+movie["key"]} for movie in api["results"]]
            api = movies
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})
    
    

def getSearchResults(request):

    if request.method == 'POST':

        movie_name = request.POST['movie_name']
        language = request.POST['language']

        url = env("API_URL")+"/3/search/multi?api_key="+env('API_KEY')+"&language="+language+"&page=1&include_adult=false&query="+movie_name
        print(url)
        headers = {'Accept': 'application/json'}
       
        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
        
            movies = [{"id": movie["id"], "original_title": movie["title"] if "title" in movie else None, "original_name": movie["name"] if "name" in movie else None} for movie in api["results"]]


            api["results"]
            api = movies
        except Exception as e:
            api = {"error": str(e)}


        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})


def getGenres(request):

    if request.method == 'POST':

        language = request.POST['language']

        url = env("API_URL")+"/3/genre/movie/list?api_key="+env('API_KEY')+"&language="+language
        headers = {'Accept': 'application/json'}
       
        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})


def getMoviesByGenre(request):

    if request.method == 'POST':

        language = request.POST['language']
        page = request.POST['num_page']
        genres_id = request.POST['genres_id']

        url = env("API_URL")+"/3/discover/movie?api_key="+env('API_KEY')+"&with_genres="+genres_id+"&language="+language+"&page="+page
        headers = {'Accept': 'application/json'}
       
        api_requests = requests.get(url, headers=headers)

        try:
            api = json.loads(api_requests.content)
            movies = [{"film_id": movie["id"], "vote_average": movie["vote_average"], "title": movie["title"], "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/"+movie["poster_path"]} for movie in api["results"]]
            api = movies
         
        except Exception as e:
            api = {"error": str(e)}

        return JsonResponse(api,safe=False,json_dumps_params={'ensure_ascii':False})


def getFilmTitleAndImage(request):

    if request.method == 'POST':

        list_content = request.POST['list_content']
        language = request.POST['language']

        json_list_content = json.loads(list_content)
        print(json_list_content)

        list_title_image = []

        for list_film in json_list_content:
            if(list_film['type'] == '0'):
                url = env("API_URL")+"/3/movie/"+list_film['id']+"?api_key="+env('API_KEY')+"&language="+language
                
                headers = {'Accept': 'application/json'}
                api_requests = requests.get(url, headers=headers)

                try:
                    api = json.loads(api_requests.content)
                    movies = [{"film_id": api["id"], "title": api["title"], "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/"+api["poster_path"]} ]
                    list_title_image.append(movies)
                except Exception as e:
                    api = {"error": str(e)}

        return JsonResponse(list_title_image,safe=False,json_dumps_params={'ensure_ascii':False})