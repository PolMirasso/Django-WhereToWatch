from django.urls import path
from . import views

urlpatterns = [
    path('getAllData/', views.getAllData, name="getAllData"),
    path('getFilmData/', views.getFilmData, name="getFilmData"),
    path('getCinemaData/', views.getCinemaData, name="getCinemaData"),
    path('getTopRatedFilms/', views.getTopRatedFilms, name="getTopRatedFilms"),
    path('getPopularFilms/', views.getPopularFilms, name="getPopularFilms"),
    path('getSimilarMovie/', views.getSimilarMovie, name="getSimilarMovie"),
    path('getProviders/', views.getProviders, name="getProviders"),
]
