import os

from fabric.api import cd, env, execute, local, prefix, run, task


env.use_ssh_config = True
env.hosts = ['rank-me.io']
env.site_user = 'rankme'
env.site_group = 'rankme'
env.project_root = '/var/www/rank-me/rankme'


def push_tag(tag):
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
            run("python manage.py syncdb")
            run("python manage.py migrate")


def install_static():
    with cd(env.project_root):
        with prefix("source ../ENV/bin/activate"):
            run("python manage.py collectstatic --noinput")


@task
def restart_process():
    gunicorn_pid = run('cat %s' % os.path.join(env.project_root,
                                               '../tmp/gunicorn.pid'))
    run('kill %s' % gunicorn_pid)


@task
def deploy(tag):
    execute(push_tag, tag=tag)

    execute(update_remote_git, tag=tag)
    execute(install_requirements)
    execute(install_static)
    execute(migrate_database)

    execute(restart_process)
