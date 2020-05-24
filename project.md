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

add dashboard/urls.py
add in project/urls.py: path('', include('dashboard.urls'))


create repository on github (public):
C:\Program Files\PuTTY
C:\Program Files\Git
git remote add origin https://github.com/satrum/alerts_dashboard.git
git push -u origin master




