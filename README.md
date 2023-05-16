
# brain_health
# WehappyAdmin

Brain Health

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Notes about development

Eslam Essam Feel free to contact me for any questions:

```bash
My Github: https://github.com/EslamEs1
Gmail: eslamdeveloper1@gmail.com
```
## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Type checks

Running type checks with mypy:

    $ mypy brain_health

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Project

This app comes with Docker.

To run a project:
there tow file for run docker local.yml and production.yml

```bash
cd brain_health
docker-compose -f filename.yml build
docker-compose -f filename.yml up -d
```

To migrations or createsuperuser:

```bash
cd brain_health
there tow file for run docker local.yml and production.yml,
docker-compose -f filename.yml build run --rm django python manage.py migrate , makemigrations , createsuperuser
```

### Celery

This app comes with Celery Redis.

To run a celery worker:

```bash
cd brain_health
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd brain_health
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd brain_health
celery -A config.celery_app worker -B -l info
```

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).


