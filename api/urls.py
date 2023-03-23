from django.urls import path
from . import views

urlpatterns = [
    path('getAllData/', views.getAllData, name="getAllData"),
    path('getFilmData/', views.getFilmData, name="getFilmData"),
    path('getCinemaData/', views.getCinemaData, name="getCinemaData"),
    path('getRecommendedFilms/', views.getRecommendedFilms, name="getRecommendedFilms"),
    path('', views.index, name="index")
]
