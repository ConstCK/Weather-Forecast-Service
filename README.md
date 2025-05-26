Проект на Django + httpx для доступа к API + scss для стилизации HTML.
Есть возможность запуска в Docker.

* Скопируйте проект к себе на ПК при помощи: git clone https://github.com/ConstCK/Weather-Forecast-Service.git
* Перейдите в папку проекта
* В терминале создайте виртуальное окружение (например python -m venv venv) и активируйте его (venv\scripts\activate)
* Установите все зависимости при помощи pip install -r requirements.txt
* Создайте файл .env в каталоге проекта "project/" и пропишите в нем данные по примеру .env.example
* SECRET_KEY можно создать следующим образом в терминале из каталога "project/":

1. python manage.py shell
2. from django.core.management import utils
3. utils.get_random_secret_key()


**Для локального запуска в консоли в каталоге проекта "project/" используйте python manage.py runserver**
**Для запуска тестов в консоли в каталоге проекта используйте python manage.py test**

**Запустите Docker Desktop на пк
В терминале из каталога проекта запустите docker-compose up для запуска в контейнере**

**Из ТЗ выполнил:**
1. Запуск приложения в Docker контейнере
2. Автозаполнение в форме последнего города для пользователя 
3. Сохранение в БД истории поиска с выдачей статистики
4. Написание тестов



