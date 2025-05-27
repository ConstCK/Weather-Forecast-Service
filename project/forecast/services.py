import datetime
from typing import Any

import httpx

from django.db.models import Count
from django.contrib.auth.models import User

from .constants import CITY_COORDS_URL, WEATHER_FORECAST_URL
from .models import ForecastRequest


class CityService:

    @staticmethod
    def get_coords_from_db(city_name: str) -> dict[str, float | None] | None:
        # Получение координат города по его названию из БД
        result = ForecastRequest.objects.filter(city=city_name)
        if result:
            return {'latitude': result[0].city_lat, 'longitude': result[0].city_lon}

    @staticmethod
    def get_coords_by_city(city_name: str) -> dict[str, str] | None:
        # Получение координат города по его названию с API
        params = {
            'name': city_name,
            'language': 'ru',
            'count': 1,
        }
        try:
            response = httpx.get(
                CITY_COORDS_URL, params=params
            ).json().get('results')[0]
            lat = response.get('latitude')
            lon = response.get('longitude')
            return {'latitude': lat, 'longitude': lon}
        except Exception:
            return None

    @staticmethod
    def last_city_info(user: User) -> str | None:
        # Получение города из последнего запроса пользователя
        result = ForecastRequest.objects.filter(user=user)
        if result:
            return result[0].city
        return None


class ForecastService:
    @staticmethod
    def get_weather_forecast(lat: str, lon: str) -> dict[str, int] | None:
        # Получение температуры на ближайший час по координатам города с API
        params = {
            'latitude': lat,
            'longitude': lon,
            'hourly': 'temperature_2m',
            'forecast_days': 1,
        }
        try:
            response = httpx.get(
                WEATHER_FORECAST_URL,
                params=params
            ).json()
            current_time = datetime.datetime.now().hour
            # Список всех временных отрезков суток
            time_list = response.get('hourly').get('time')
            # Перевод в datetime формат
            time_obj_list = list(
                map(
                    lambda x: datetime.datetime.strptime(
                        x, '%Y-%m-%dT%H:%M'
                    ), time_list
                )
            )
            # Выбор часа больше текущего
            forecast_time = [
                x for x in time_obj_list if x.hour > current_time][0]
            forecast_hour = forecast_time.hour
            # Выбор температуры на ближайший час
            forecast_temp = response.get('hourly').get(
                'temperature_2m'
            )[forecast_hour]
            return {'hour': forecast_hour, 'temperature': forecast_temp}

        except Exception:
            return None

    @staticmethod
    def add_data_to_db(user: User, city_name: str, lat: str, lon: str, ) -> None:
        # Добавление запроса погоды в БД
        ForecastRequest.objects.create(
            user=user, city=city_name, city_lat=lat, city_lon=lon
        )

    @staticmethod
    def get_main_statistic(user: User) -> list[dict[str, str | datetime.datetime]] | None:
        # Получение общей статистики запросов пользователя
        query = ForecastRequest.objects.filter(user=user)
        if query:
            result = [x for x in query.values('city', 'created_at')]
            return result
        return None

    @staticmethod
    def get_city_statistic(user: User) -> list[dict[str, str | int]] | None:
        # Получение статистики по количеству запросов для каждого города пользователя
        query = ForecastRequest.objects.filter(user=user).values('city')
        if query:
            query = query.annotate(
                city_count=Count('city')
            ).order_by('-city_count')
            result = [x for x in query]
            return result
        return None
