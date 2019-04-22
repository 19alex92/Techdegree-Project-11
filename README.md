# Treehouse Techdegree-Project-11

## Project Description

Create the models, serializers, and views to power the provided Angular
application. You can check through the supplied JavaScript to see what
resources should be available or check below. You are allowed to change,
extend, and improve the JavaScript if desired, but the final result must still
meet all of the required features/abilities.

## Installing / Getting started

### With virtual env

```shell
pip install -r requirements.txt
```

### With Pipenv

> Installs from Pipfile.lock

```shell
pipenv install
```

## Import Dogs

If you need to import dogs, a `data_import` script has been provided.

## Run the server

```shell
python manage.py runserver
```

## Testing Coverage

1. Run the tests

```shell
coverage run manage.py test pugorugh
```

2. Get a report

```shell
coverage report
```

3. For a html report

```shell
coverage html
```

## Routes

The following routes are provided for the JavaScript application.

* To get the next liked/disliked/undecided dog

	* `/api/dog/<pk>/liked/next/`
	* `/api/dog/<pk>/disliked/next/`
	* `/api/dog/<pk>/undecided/next/`

* To change the dog's status

	* `/api/dog/<pk>/liked/`
	* `/api/dog/<pk>/disliked/`
	* `/api/dog/<pk>/undecided/`

* To change or set user preferences

	* `/api/user/preferences/`

