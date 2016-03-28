Installation
============

Run the following command::

    vagrant up

This will create a box and install everything you need. Once it's installed,
use ``vagrant ssh`` to SSH to the box and run ``./manage.py runserver`` to run
the development server. You'll then be able to connect to
http://rank-me.lo/.

You'll probably want to run ``./manage.py createsuperuser`` to create a super
user and then login on ``/admin/``, sparing the need to setup Twitter
authentication (see below).

Assets management
~~~~~~~~~~~~~~~~~

Install Sass and Compass::

    bundle install

Make sure you have grunt and bower installed::

    npm install -g bower grunt grunt-cli

Install project dependencies::

    npm install
    bower install

Compute Sass with grunt::

    # compile once
    grunt compass

    # keep looking at changes and recompile when needed
    grunt

Twitter authentication
======================

Most of the application requires to be authenticated. This means you'll get
redirected to Twitter if you try to access a protected page. If you don't want
to register a Twitter app to get an API key and secret, you can just create a
user with ``./manage.py createsuperuser``, go to ``/admin`` and log in. Once you're
authenticated, you'll be able to go through the whole application.

API documentation
=================

Go to http://rank-me.lo/api

Deployment
==========

* Create a git tag
* fab deploy:{{tag}}

Contribute
==========

Any contribution welcome! Ideally use pull requests and make sure that the
tests still pass (see above).

We use the Github issues as a Backlog.
