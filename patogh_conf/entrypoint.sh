python manage.py collectstatic --noinput

# python manage.py makemigrations

python manage.py migrate

gunicorn patogh.wsgi:application --bind 0.0.0.0:8000
