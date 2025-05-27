from django.urls import path
from .views import city_autocomplete, main, main_statistic, about, city_statistic

urlpatterns = [
    path('', main, name='main'),
    path('main-statistic/', main_statistic, name='main_statistic'),
    path('city-statistic/', city_statistic, name='city_statistic'),
    path('about/', about, name='about'),
    path('autocomplete/city/', city_autocomplete, name='city-autocomplete'),
]
