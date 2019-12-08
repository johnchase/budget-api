install:
	pip install -r requirements.txt

build:
	python manage.py makemigrations
	python manage.py migrate

serve:
	python manage.py runserver

test: 
	python manage.py test && flake8 --max-line-length 119 --exclude=migrations,config
