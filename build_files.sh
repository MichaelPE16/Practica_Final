#!/bin/bash
python3 -m pip install -r requirements.txt --break-system-packages --root-user-action=ignore
python manage.py collectstatic --noinput --clear
python manage.py makemigrations
python manage.py migrate
