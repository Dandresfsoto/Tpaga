from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = env(
    "SECRET_KEY",
    default="336-ya3kd#q^c_osm@96z!6skgt6sew#efrhdod30iuqd2gfc@",
)

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('POSTGRES_DB'),
            'USER': env('POSTGRES_USER'),
            'PASSWORD': env('POSTGRES_PASSWORD'),
            'HOST': env('POSTGRES_HOST'),
            'PORT': env('POSTGRES_PORT'),
        }
}
