# LITREVIEW

## Installation

Voici les quelques étapes à suivre pour que vous puissiez pleinement tester le
projet  
A la racine du projet :

- `python3 -m venv env` pour créer un environnement virtuel
- `source env/bin/activate` pour activer l'environnement

Une fois que l'environnement est activé, SI vous souhaitez démarrer
l'application de 0 :

- `python manage.py makemigrations` pour s'assurer qu'il ne manque aucune
  migration dans le projet
- `python manage.py migrate` pour effectuer les migrations et créer la base de
  données locale

## Lancement de l'application

Pour pouvoir tester le projet en local, à la racine du projet :

- `python manage.py runserver`

## Identifiants de tests

- Username: test
- password: thisisatest

Enjoy :D

------------ 

## Installation

Here are the steps to follow so that you can fully test the project.
At the root of the project:

- `python3 -m venv env` to create a virtual environment
- `source env/bin/activate` to activate the environment

Once the environment is activated:

- `python manage.py makemigrations` to ensure no migrations are missing in the
  project
- `python manage.py migrate` to perform the migrations and create the local
  database

## Launching the Application

To test the project locally, at the root of the project:

- `python manage.py runserver`

On the first launch, you will not have any users created nor tickets/reviews,
as the project will be entirely blank since the database is local

Enjoy :D
