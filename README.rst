Installation
============

(optional) create a virtualenv with virtualenvwrapper::

    mkvirtualenv rankme

Start by installing the requirements and set up your database::

    pip install -r requirements/dev.txt
    # Put your database URL in here in the form postgres://user:password@host/dbname or sqlite:////absolute/path
    vim envdir/DATABASE_URL

Create the database::

    ./manage.py syncdb
    ./manage.py migrate

Then run the development server::

    ./manage.py runserver


To run the tests::

    ./manage.py test

Twitter authentication
======================

Most of the application requires to be authenticated. This means you'll get
redirected to Twitter if you try to access a protected page. If you don't want
to register a Twitter app to get an API key and secret, you can just create a
user with ``./manage.py createsuperuser``, go to ``/admin`` and log in. Once you're
authenticated, you'll be able to go through the whole application.

API documentation
=================

Go to http://127.0.0.1:8000/api

Assets management
=================

Make sure you have grunt and bower installed::

    npm install -g bower grunt grunt-cli

Install project dependencies::

    npm install
    bower install

Compute LESS with grunt::

    # compile once
    grunt less

    # keep looking at changes and recompile when needed
    grunt

Deployment
==========

* Create a git tag
* fab deploy:{{tag}}

Available settings
==================

The following list contains the settings that can be set with environment
variables. To set such a setting, create a file that has the same name as the
setting in the ``envdir`` directory (for example if you want to override the
``DEBUG`` setting, create a file named ``envdir/DEBUG`` and put the value of the
setting in the file).

* ALLOWED_HOSTS (1 host / line)
* DATABASE_URL (see https://github.com/kennethreitz/dj-database-url for the syntax)
* DEBUG (put an empty string in the file to set DEBUG to false, or 1 to set it to true)
* SECRET_KEY
* STATIC_ROOT
* STATIC_URL
* SOCIAL_AUTH_TWITTER_KEY
* SOCIAL_AUTH_TWITTER_SECRET
* SLACK_API_TOKEN

Contribute
==========

Any contribution welcome! Ideally use pull requests and make sure that the tests still pass (see above).

We use the Github issues as a Backlog.
