# Foodies

Developed using Test-Driven-Development and [Docker](https://docs.docker.com/compose/django/)

### 📖 Install

```
$ git clone https://github.com/ycv005/foodies.git
$ cd getnote

# Run Migrations
$ python manage.py migrate

# Create a Superuser:
$ python manage.py createsuperuser

# Confirm everything is working:
$ python manage.py runserver

# Load the site at http://127.0.0.1:8000
```

To make your code ready for PEP8 coding style, use [autopep8](https://github.com/hhatto/autopep8) along with following command-

```
autopep8 --in-place --aggressive --aggressive <filename>
```

Test your code against all unit test and flake8-

```
docker-compose run --rm app sh -c "python manage.py test && flake8"
```