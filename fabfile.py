from contextlib import nested
from datetime import datetime
import os

import dj_database_url
from fabric.api import (
    cd, env, execute, get, local, prefix, run, settings, shell_env, task
)
from fabric.context_managers import quiet


env.use_ssh_config = True
env.hosts = ['rank-me.io']
env.site_user = 'rankme'
env.site_group = 'rankme'
env.project_root = '/var/www/rank-me/rankme'


def push_tag(tag):
    with settings(warn_only=True):
        local("git push -f origin %s" % tag)


def checkout_tag(tag):
    local("git checkout %s" % tag)


def update_remote_git(tag):
    with cd(env.project_root):
        run("git fetch -t -p")
        run("git checkout %s" % tag)


def install_requirements():
    with cd(env.project_root):
        with prefix("source ../ENV/bin/activate"):
            run("pip install -r requirements/base.txt")


def migrate_database():
    with cd(env.project_root):
        with prefix("source ../ENV/bin/activate"):
            run("python manage.py migrate")


def install_static():
    with cd(env.project_root):
        with prefix("source ../ENV/bin/activate"):
            run("python manage.py collectstatic --noinput")


@task
def restart_process():
    with cd(env.project_root):
        run('touch rankme/wsgi.py')


@task
def compile_css():
    with cd(env.project_root):
        run('npm install')
        run('gulp build --production')


@task
def deploy(tag):
    execute(push_tag, tag=tag)

    execute(update_remote_git, tag=tag)
    execute(install_requirements)
    execute(compile_css)
    execute(install_static)
    execute(migrate_database)

    execute(restart_process)


@task
def fetch_db(destination='.'):
    """
    Dump the database on the remote host and retrieve it locally.

    The destination parameter controls where the dump should be stored locally.
    """
    with nested(cd(env.project_root), quiet()):
        db_credentials = run('cat envdir/DATABASE_URL')
    db_credentials_dict = dj_database_url.parse(db_credentials)

    if not is_supported_db_engine(db_credentials_dict['ENGINE']):
        raise NotImplementedError(
            "The fetch_db task only supports postgresql databases"
        )

    outfile = datetime.now().strftime('%Y-%m-%d_%H%M%S.sql.gz')
    outfile_remote = os.path.join('~', outfile)

    with shell_env(PGPASSWORD=db_credentials_dict['PASSWORD'].replace('$', '\$')):
        run('pg_dump -O -x -h {host} -U {user} {db}|gzip > {outfile}'.format(
            host=db_credentials_dict['HOST'],
            user=db_credentials_dict['USER'],
            db=db_credentials_dict['NAME'],
            outfile=outfile_remote))

    get(outfile_remote, destination)
    run('rm %s' % outfile_remote)

    return outfile


@task
def import_db(dump_file=None):
    """
    Restore the given database dump.

    The dump must be a gzipped SQL dump. If the dump_file parameter is not set,
    the database will be dumped and retrieved from the remote host.
    """
    with open('envdir/DATABASE_URL', 'r') as db_credentials_file:
        db_credentials = db_credentials_file.read()
    db_credentials_dict = dj_database_url.parse(db_credentials)

    if not is_supported_db_engine(db_credentials_dict['ENGINE']):
        raise NotImplementedError(
            "The import_db task only supports postgresql databases"
        )

    if dump_file is None:
        dump_file = fetch_db()

    db_info = {
        'host': db_credentials_dict['HOST'],
        'user': db_credentials_dict['USER'],
        'db': db_credentials_dict['NAME'],
        'db_dump': dump_file
    }

    with shell_env(PGPASSWORD=db_credentials_dict['PASSWORD']):
        with settings(warn_only=True):
            local('dropdb -h {host} -U {user} {db}'.format(**db_info))

        local('createdb -h {host} -U {user} {db}'.format(**db_info))
        local('gunzip -c {db_dump}|psql -h {host} -U {user} {db}'.format(
            **db_info
        ))


def is_supported_db_engine(engine):
    return engine == 'django.db.backends.postgresql_psycopg2'
