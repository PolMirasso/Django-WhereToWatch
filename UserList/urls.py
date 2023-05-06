from django.urls import path
from . import views

urlpatterns = [
    path('createList/', views.createList.as_view(), name='createList'),
    path('getUserLists/', views.getUserLists.as_view(), name='getUserLists'),

]
