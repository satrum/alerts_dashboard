from sources:

    git clone https://github.com/satrum/alerts_dashboard.git %project_folder%
    cd %project_folder%
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r backend/requirements.txt

setup:

    pip install django
    pip install djangorestframework
    pip install psycopg2 OR psycopg2-binary
    pip install django-debug-toolbar
    pip install django-colorfield
    cd backend
    pip freeze > requirements.txt
    django-admin startproject project .
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8800
    python manage.py startapp dashboard
    settings.py: INSTALLED_APPS 'dashboard'
    settings.py: INSTALLED_APPS 'rest_framework'
    settings.py: INSTALLED_APPS 'debug_toolbar'
    settings.py: INSTALLED_APPS 'colorfield'
    settings.py: ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.1.1.132']
    settings.py:
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10
    }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dashboard_db',
            'USER': 'dashboard_user',
            'PASSWORD': 'dashboard_password',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
    INTERNAL_IPS = ['127.0.0.1', 'localhost', ]


add superuser:

    python manage.py createsuperuser --email admin@localhost --username admin (password:12345678)

urls:

    add dashboard/urls.py
    add in project/urls.py: path('', include('dashboard.urls'))


create repository on github (public):

    C:\Program Files\PuTTY
    C:\Program Files\Git
    git remote add origin https://github.com/satrum/alerts_dashboard.git
    git push -u origin master



__что необходимо сделать__

*сессия*
```
клиент подключается к API , получает cookies , вместе session_id
при создании Results необходимо передавать session_id (cookies)
при входе пользователя в профиль - должна сохраняться его история
при создании пользователя - необходимо привязать все Results в его текущей сессии

1 способ:
метод GET /check_session headers=cookies

A проверяем текущего пользователя
B1 
если не авторизован и не создавался пользователь - создаем нового пользователя
    from django.contrib.auth.models import User
    # Создайте пользователя и сохраните его в базе данных
    user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
    # Обновите поля и сохраните их снова
    user.first_name = 'John'
    user.last_name = 'Citizen'
    user.save()
добавляем в request.session['user'] = generated_username, request.session['password'] = generated_password
B2
если не авторизован и request.session.get('user', None) is not None -> D

D авторизуем его автоматически
E POST /create_Result требует авторизации
F пользователю предлагается на экране сделать постоянную учетку, указав email , на который будет отправлен текущий user/password и ссылка на форму смена пароля.

2 способ:
POST /create_Result требует наличия cookies , в таблице Results.session_id = записывается session_pk
пользователю предлагается на экране сделать учетку, указав email+пароль или Oauth
пользователь создается и авторизуется
автоматически ко всем Results с текущим session_id добавляется user_id
```

**методы дашборда**

*Получение списка категорий:*

GET http://10.1.1.132:8800/category_list/

авторизация не нужна
возвращает cookies с sessionid, который надо использовать в дальнейшем

*Получение списка опросов (всех без паджинации):*

GET http://10.1.1.132:8800/poll_list/

авторизация не нужна

*Получение списка результатов:*

GET http://10.1.1.132:8800/result_list/?poll_id=1

GET http://10.1.1.132:8800/result_list/

необходимо cookies с sessionid, иначе возвращает 401

фильтрует по sessionid и по Poll.id , т.е. выдает список результатов данной сессии и опроса

*Пройти опрос:*

POST http://10.1.1.132:8800/result/

{
    "result": 
        {
            "poll": 3,
            "result": [
                "Кошка", "Собака"
            ],
            "input_text": "Не нашел среди вариантов попугая",
            "user": null
        }
}

Results.create(poll_id, session_id, -user_id, result, -input_text).save()
ОК требуется cookies
ОК проверяется session_id, и добавляется в Result.session_key
OK проверяется на тип опроса и соответствие Poll.options/Poll.type и Result.result
проверяется на уникальность (был ли уже ответ, и можно ли повторить)
проверять поле Poll.another, Poll.another_text и Result.input_text
!!! проверяется user_id - позже

*Получить статистики:*

- статистика по опросу 
    - распределение вариантов ответов за все время (О, М)
    - процент ответивших от всех сессий (А, О, М)
    - распределение количества всех ответов по дням (А, О, М)
    - распределение количества ответов по вариантам по дням (А, О, М)
- статистика коррелиций опроса с другим опросом
    - матрица корреляций между вариантами ответов двух разных опросов (А, О, М)
- геораспределение по регионам (используя ip)
    - по одному опросу, количество ответов суммарное и по вариантам ответов

**категории**

- личное
- здоровье
- работа
- общество
- покупки
- путешествия
- идентификация

- веселая математика
- covid
- игры
- секс
- промо (бренд)


#### Срочно
1. - валидация POST view.PollView (категория существует, список вариантов - непустой)
2. авторизация по сессии, для получения и обновления Cookies
3. !!! отдельный GET view 'create_session' возвращающий cookies с sessionid (убрать из category_list/)
4. ->!!! POST view 'result' для создания ответа 