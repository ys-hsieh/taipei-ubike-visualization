from django.urls import path

from . import views, scraper

urlpatterns = [
    path('', views.index, name='index'),
    path('counter', views.counter, name='counter'),
    path('count', views.count, name='count'),
    path('show', scraper.show, name='show'),
    path('fetch', scraper.fetchTaipeiYouBikeAPIData, name='fatch'),
    path('fetchUbikeStopData', scraper.fetchUbikeStopDataFromAPI, name='fetchUbikeStopDataFromAPI'),
    path('fetchStopStatusData', scraper.fetchStopStatusDataFromAPI, name='fetchStopStatusDataFromAPI'),
]