from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render

from .constants import MESSAGES
from .models import ForecastRequest
from .services import CityService, ForecastService
from .forms import ForecastRequestForm

city_service = CityService()
forecast_service = ForecastService()


def main(request):
    try:
        user = User.objects.get(username=request.user)
        last_city = city_service.last_city_info(user)
    except ObjectDoesNotExist:
        last_city = ''

    form = ForecastRequestForm({'city': last_city})
    if request.method == "POST":
        form = ForecastRequestForm(request.POST)
        if form.is_valid():
            result = None
            user = User.objects.get(username=request.user)
            city = request.POST.get('city')
            # Проверка есть ли координаты города в БД и добавление данных в случае отсутствия
            if city_service.get_coords_from_db(city):
                result = forecast_service.get_weather_forecast(
                    str(city_service.get_coords_from_db(city).get('latitude')),
                    str(city_service.get_coords_from_db(city).get('longitude'))
                )
                forecast_service.add_data_to_db(
                    user,
                    city,
                    str(city_service.get_coords_from_db(city).get('latitude')),
                    str(city_service.get_coords_from_db(city).get('longitude'))
                )

            else:
                coords = city_service.get_coords_by_city(city)
                if coords:
                    lat = coords.get('latitude')
                    lon = coords.get('longitude')

                    forecast_service.add_data_to_db(
                        user,
                        city,
                        str(lat),
                        str(lon)
                    )

                    result = forecast_service.get_weather_forecast(lat, lon)

            if result:
                return render(
                    request, 'main.html',
                    context={
                        'city': city,
                        'hour': result.get('hour'),
                        'temperature': result.get('temperature'),
                        'form': form,
                        'title': MESSAGES.get('main_header')
                    }
                )
            return render(
                request, 'main.html',
                context={
                    'form': form,
                    'error': MESSAGES.get('no_city_error')
                }
            )

    return render(
        request, 'main.html',
        context={'form': form, 'title': MESSAGES.get('main_header')}
    )


def main_statistic(request):
    # Получение основной статистики по запросам погоды для пользователя
    try:
        user = User.objects.get(username=request.user)
        stat = forecast_service.get_main_statistic(user)
    except ObjectDoesNotExist:
        stat = ''

    return render(
        request, 'main_statistic.html',
        context={
            'title': MESSAGES.get('main_statistic_header'),
            'statistic': stat
        }
    )


def city_statistic(request):
    # Получение статистики по запросам погоды для пользователя для каждого города
    try:
        user = User.objects.get(username=request.user)
        stat = forecast_service.get_city_statistic(user)
    except ObjectDoesNotExist:
        stat = ''

    return render(
        request, 'city_statistic.html',
        context={
            'title': MESSAGES.get('city_statistic_header'),
            'statistic': stat
        }
    )


def about(request):
    return render(
        request,
        'about.html',
        context={'title': MESSAGES.get('about_header')}
    )


def city_autocomplete(request):
    query = request.GET.get('q', '')
    cities = (
        ForecastRequest.objects.filter(user=request.user, city__icontains=query)
        .values_list('city', flat=True)
    )
    cities = set(cities)
    return JsonResponse(list(cities), safe=False)
