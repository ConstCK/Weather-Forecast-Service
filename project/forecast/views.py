from django.contrib.auth.models import User
from django.shortcuts import render

from .services import CityService, ForecastService
from .forms import ForecastOrderForm

city_service = CityService()
forecast_service = ForecastService()


def main(request):
    try:
        user = User.objects.get(username=request.user)
        last_city = city_service.last_city_info(user)
    except Exception:
        last_city = ''

    form = ForecastOrderForm({'city': last_city})
    if request.method == "POST":
        form = ForecastOrderForm(request.POST)
        if form.is_valid():
            result = None
            user = User.objects.get(username=request.user)
            city = request.POST.get('city')
            # Проверка есть ли координаты города в БД и добавление нового запроса
            if city_service.get_coords_from_db(city):
                result = forecast_service.get_weather_forecast(
                    str(city_service.get_coords_from_db(city).get('latitude')),
                    str(city_service.get_coords_from_db(city).get('longitude'))
                )
                # forecast_service.add_data_to_db(
                #     user,
                #     city,
                #     str(
                #         city_service.get_coords_from_db(city).get('latitude')
                #         ),
                #     str(
                #         city_service.get_coords_from_db(city).get('longitude')
                #         )
                #     )

            else:
                coords = city_service.get_coords_by_city(city)
                if coords:
                    lat = coords.get('latitude')
                    lon = coords.get('longitude')
                    result = forecast_service.get_weather_forecast(lat, lon)

                    forecast_service.add_data_to_db(
                        user,
                        city,
                        str(lat),
                        str(lon)
                        )

            if result:
                return render(
                    request, 'main.html',
                    context={
                        'city': city,
                        'hour': result.get('hour'),
                        'temperature': result.get('temperature'),
                        'form': form,
                        'title': 'Welcome to weather forecast!'
                    }
                    )
            return render(
                request, 'main.html',

                context={
                    'form': form,
                    'error': 'Указанный город не найден'
                }
            )
    return render(
        request, 'main.html',
        context={'form': form, 'title': 'Welcome to weather forecast!'}
        )


def main_statistic(request):
    try:
        user = User.objects.get(username=request.user)
        stat = forecast_service.get_main_statistic(user)
    except Exception:
        stat = " "
    return render(
        request, 'main_statistic.html',
        context={
            'title': 'Основная статистика запросов',
            'statistic': stat
        }
        )


def city_statistic(request):
    try:
        user = User.objects.get(username=request.user)
        stat = forecast_service.get_city_statistic(user)
    except Exception:
        stat = " "
    return render(
        request, 'city_statistic.html',
        context={
            'title': 'Статистика запросов по городам',
            'statistic': stat
        }
        )


def about(request):
    return render(request, 'about.html', context={'title': 'About page'})
