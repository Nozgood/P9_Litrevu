env:
	source env/bin/activate

make-migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver
