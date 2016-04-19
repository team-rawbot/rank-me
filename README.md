# Rank-me.io

## Installation

Run the following command::

    vagrant up

This will create a box and install everything you need. Once it's installed, use `vagrant ssh` to SSH to the box and run `./manage.py runserver` to run the development server. You'll then be able to connect to http://rank-me.lo/.

### Create admin account

You'll probably want to run `./manage.py createsuperuser` to create a super user and then login on `/admin/`, sparing the need to setup Twitter authentication (see below).

### Assets management

Build assets and watch for changes by running the following command inside the box:

    gulp

## Twitter authentication

Most of the application requires to be authenticated. This means you'll get redirected to Twitter if you try to access a protected page. If you don't want to register a Twitter app to get an API key and secret, you can just create a user with ``./manage.py createsuperuser``, go to ``/admin`` and log in. Once you're authenticated, you'll be able to go through the whole application.

## API documentation

Go to [rank-me.lo/api](http://rank-me.lo/api)

## Deployment

* Create a Git tag
* `fab deploy:{{tag}}`

## Running the tests

To run the tests, make sure test dependencies are installed by running the
following command in the box:

    pip install -r requirements/test.txt

And then run the tests with the following command (again, in the box):

    ./runtests.sh

To run a specific test, use [the same syntax as you would with ``manage.py test``](https://docs.djangoproject.com/en/stable/topics/testing/overview/#running-tests>):

    ./runtests apps.game.tests.functional.test_competition.TestCompetition.test_create_competition

## Contribute

Any contribution welcome! Ideally use pull requests and make sure that the
tests still pass.

We use the [Github issues](https://github.com/team-rawbot/rank-me/issues) as a backlog.
