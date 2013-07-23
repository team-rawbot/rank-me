Installation
============

Start by installing the requirements and copy the settings file::

    pip install -r requirements.txt
    cp rankme/settings/local.py.dist rankme/settings/local.py

Edit the `DATABASE_SETTINGS` to match your local setup.

Create the database::

    ./manage.py syncdb --all
    ./manage.py migrate --fake

Then run the development server::

    ./manage.py runserver
