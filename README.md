# blog

Just my personal blogging app.

## Running

If you actually want to run this yourself, you'll need poetry and then run:

    poetry install

This blog uses sqlite by default which is sufficient for my purposes. We'll need to run the migrations:

    poetry run ./manage.py migrate

Then we start the dev server and look at the site:

    poetry run ./manage.py runserver

You might also want to create a superuser to actually be able to edit posts:

    poetry run ./manage.py createsuperuser

To run the tests, do

    poetry run ./manage.py test
