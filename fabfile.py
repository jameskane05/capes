import json
from datetime import date

import requests
from fabric.api import *
from fabvenv import virtualenv, make_virtualenv

__author__ = 'Michael Spencer'

env.virtualenv_dir = '/home/qalelander/.virtualenvs/capes'

env.roledefs = {
    'web': ['qalelander@capes.lelander.com']
}


@task
@roles('web')
def manage(command):
    with cd('/var/www/site'):
        with virtualenv(env.virtualenv_dir):
            run('python manage.py ' + command)


def post_slack_message(message):
    url = 'https://hooks.slack.com/services/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'
    data = {
        'text': message,
        'channel': '#capes'
    }
    requests.post(url, data=json.dumps(data))


@task
def deploy():
    execute(update)
    post_slack_message('New version deployed to <capes.lelander.com>')

@task
@roles('web')
def bootstrap():
    # Create the virtualenv
    make_virtualenv(env.virtualenv_dir, dependencies=['pip-tools'])

    # Create the git repository
    sudo('mkdir -p /var/repo/site.git')
    sudo('chown www-data:www-data -R /var/repo')
    sudo('chmod g+rwX -R /var/repo')

    with cd('/var/repo/site.git'):
        run('git init --bare')
        put('post-receive.hook', 'hooks/post-receive')
        run('chmod +x hooks/post-receive')

    # Set up the site directory
    run('mkdir -p /var/www/site')
    sudo('chown www-data:www-data -R /var/www')
    sudo('chmod g+rwX -R /var/www')

    # Set up nginx
    sudo('rm /etc/nginx/sites-enabled/default', quiet=True)


@task
@roles('web')
def update():
    # Make sure the post-receive hook is up-to-date
    with cd('/var/repo/site.git'):
        sudo('chown qalelander:qalelander -R .')
        put('post-receive.hook', 'hooks/post-receive')
        run('chmod +x hooks/post-receive')

    # Push the server
    local('git push live master --force')
    run('git --work-tree=/var/www/site --git-dir=/var/repo/site.git checkout -f')

    # Update the nginx and upstart config
    with cd('/var/www/site'):
        sudo('cp capes.nginx /etc/nginx/sites-available/capes')
        sudo('cp capes.conf /etc/init/capes.conf')
        sudo('ln -s /etc/nginx/sites-available/capes /etc/nginx/sites-enabled', quiet=True)

        with virtualenv(env.virtualenv_dir):
            # Update pip dependencies
            run('pip-sync')

            # Migrate the database if necessary
            run('python manage.py collectstatic --noinput')

    # Restart the upstart and nginx services
    sudo('sudo service nginx reload')
    sudo('sudo service capes restart')
