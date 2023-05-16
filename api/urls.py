from django.urls import path
from . import views

urlpatterns = [
    #path('getAllData/', views.getAllData, name="getAllData"),
    path('getFilmDataCinema/', views.getFilmDataCinema, name="getFilmDataCinema"),
    path('getFilmData/', views.getFilmData, name="getFilmData"),
    path('getCinemaData/', views.getCinemaData, name="getCinemaData"),
    path('getTopRatedFilms/', views.getTopRatedFilms, name="getTopRatedFilms"),
    path('getPopularFilms/', views.getPopularFilms, name="getPopularFilms"),
    path('getSimilarMovie/', views.getSimilarMovie, name="getSimilarMovie"),
    path('getSeriesData/', views.getSeriesData, name="getSeriesData"),
    path('getSeriesProviders/', views.getSeriesProviders, name="getSeriesProviders"),
    path('getSeriesSimilars/', views.getSeriesSimilars, name="getSeriesSimilars"),
    path('getProviders/', views.getProviders, name="getProviders"),
    path('getAlternativeTitles/', views.getAlternativeTitles, name="getAlternativeTitles"),
    path('getMovieRecommendations/', views.getMovieRecommendations, name="getMovieRecommendations"),
    path('getMovieVideos/', views.getMovieVideos, name="getMovieVideos"),
    path('getSearchResults/', views.getSearchResults, name="getSearchResults"),
    path('getUpcomingFilms/', views.getUpcomingFilms, name="getUpcomingFilms"),
    path('getGenres/', views.getGenres, name="getGenres"),
    path('getMoviesByGenre/', views.getMoviesByGenre, name="getMoviesByGenre"),
    path('getFilmTitleAndImage/', views.getFilmTitleAndImage, name="getFilmTitleAndImage"),
    path('getSeriesGenres/', views.getSeriesGenres, name="getSeriesGenres"),
    path('getSeriesByGenre/', views.getSeriesByGenre, name="getSeriesByGenre"),
]
