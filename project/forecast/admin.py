from django.contrib import admin

from .models import ForecastRequest


class ForecastAdmin(admin.ModelAdmin):
    fields = ['user', 'city', 'city_lat', 'city_lon', 'created_at']
    readonly_fields = ['created_at']


admin.site.register(ForecastRequest, ForecastAdmin)
