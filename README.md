# LITREVIEW

## Installation

Voici les quelques étapes à suivre pour que vous puissiez pleinement tester le
projet  
A la racine du projet :

- `python3 -m venv env` pour créer un environnement virtuel
- `source env/bin/activate` pour activer l'environnement
- `pip install -r requirements.txt` pour installer les différentes dépendances

Ici une base de données locale est déjà présente, mais si vous souhaitiez
repartir de 0 :

- `python manage.py makemigrations` pour s'assurer qu'il ne manque aucune
  migration dans le projet
- `python manage.py migrate` pour effectuer les migrations et créer la base de
  données locale

Pour créer un superuser:

- `python manage.py createsuperuser`puis suivre les instructions sur le
  terminal

## Lancement de l'application

Pour pouvoir tester le projet en local, à la racine du projet :

- `python manage.py runserver`

Identifiants de connexion :

- Username : test
- password: thisisatest

Enjoy :D

------------ 

# LITREVIEW

## Installation

Here are the steps to follow so that you can fully test the project.
At the root of the project:

- `python3 -m venv env` to create a virtual environment
- `source env/bin/activate` to activate the environment
- `pip install -r requirements.txt` to install dependencies

Here, a local database is already present, but if you wish to start from
scratch:

- `python manage.py makemigrations` to ensure no migrations are missing in the
  project
- `python manage.py migrate` to perform the migrations and create the local
  database

To create a superuser:

- `python manage.py createsuperuser` then follow the instructions in the
  terminal

## Launching the Application

To test the project locally, at the root of the project:

- `python manage.py runserver`

Login credentials:

- Username: test
- Password: thisisatest

Enjoy :D
