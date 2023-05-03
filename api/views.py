from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup as bs
from django.http import JsonResponse
import json
import environ
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)


# Scrapping


def getFilmDataCinema(request):
    

    if request.method == 'POST':

        film_name = request.POST['film_name']
        film_date = request.POST['film_date']

        #-20230308

        url = env('Scraping_URL')+"peliculas/"+film_name+"/cartelera/"+film_date+"/"

        print(url)

        r = requests.get(url)
        soup = bs(r.content, features="html.parser")

        nom_ubi = [span.find('h3').text for span in soup.findAll('span', {'class': 'stprov'})]
        codis_ubis = [span['rel'] for span in soup.findAll('span', {'class': 'stprov'})]
        film_id = soup.find('div', {'id': 'showtimes'})['rel']


        data = dict(zip(nom_ubi, codis_ubis))
        data['film_id'] = film_id

        json_obj = json.dumps(data, ensure_ascii=False)

        return HttpResponse(json_obj)


def getCinemaData(request):

    if request.method == 'POST':
        

        film_id = request.POST['film_id']
        idprov = request.POST['idprov']
        nameprov = request.POST['nameprov']
        date = request.POST['date'] # ex 2023-03-08


        dades_pelicules = []

        url = env('Scraping_URL')+"controlador/films/_filmlistingscities.php?idprov="+idprov+"&fecha="+date+"&idpeli="+film_id
        
        
        r = requests.get(url)
        soup = bs(r.content, features="html.parser")

        nom_provincies = [span.find('h4').text for span in soup.findAll('span', {'class': 'stcity'})]
        
        nom_provincies_filtered = [s.split(' (')[0] for s in nom_provincies]

        idcity = [span['rel'] for span in soup.findAll('span', {'class': 'stcity'})]


        for j in range(len(nom_provincies_filtered)):



            url3 = env('Scraping_URL')+"controlador/films/_filmlistingscinemas.php?idcity="+idcity[j]+"&fecha="+date+"&idpeli="+film_id

            r3 = requests.get(url3)
            soup3 = bs(r3.content, features="html.parser")


            div_infocine = [div for div in soup3.findAll('div', {'class': 'wrapshowtimes'})]

            values_array = [nom_provincies_filtered[j]]

            for div in div_infocine:
                values = div.text.strip().split('\n\n\n\n')

                address = nameprov +' '+ values[0]

                print(address)

                values_hours = []

                for v in values:
                    mod_hours = v.replace('\n\n\n',',')
                    mod_hours = mod_hours.replace('\n','')

                    values_hours.append(mod_hours)

                values_array.append(values_hours)

            dades_pelicules.append(values_array)

        json_obj = json.dumps(dades_pelicules, ensure_ascii=False)

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
    
