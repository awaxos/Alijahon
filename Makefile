mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

user:
	python3 manage.py createsuperuser

run:
	python3 manage.py runserver

10.10.3.171:8000