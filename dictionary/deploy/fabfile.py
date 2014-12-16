from fabric.api import run, settings, env, cd, lcd, prompt, local
from fabric.contrib.console import confirm

root_path = '/Users/lballard/'
env.hosts = ['pds-rings-tools.seti.org']

prod_deploy_dir = 'dictionary'
git_branch = 'master'

def push():
    """
    pushes code to repo and pushes repo to staging
    """

    # then checkout code from repo in another directory, and transfer that copy to server
    with lcd('/Users/lballard/'):
        # checks out git repo into local dir /users/lballard/.
        # then rsyncs that copy to production

        # clean up old deploys
        local('rm -rf dictionary')

        # grab the local repo (this is all because couldn't grab remote from server)
        local('git clone -b ' + git_branch + ' file:////Users/lballard/projects/dictionary')

        if prod_deploy_dir != 'dictionary':
            local('rm -rf %s' % prod_deploy_dir)
            local('mv dictionary %s' % prod_deploy_dir) # rename it down here before rsyncing it

        # rsync that code to dev directory on production
        local('rsync -r -vc -e ssh --exclude .git --exclude static_media %s lballard@pds-rings-tools.seti.org:~/.' % prod_deploy_dir)


def deploy():
    """
    take a backup of the currently deployed source on the server
    """
    with cd('/home/lballard/'):
        # first take a backup:
        run('sudo rsync -r -vc --exclude logs /home/django/djcode/' + prod_deploy_dir + ' backups/.')

        # go
        run('sudo rsync -r -vc --exclude logs ' + prod_deploy_dir + ' /home/django/djcode/.')
        run('sudo touch /home/django/djcode/' + prod_deploy_dir + '/*.wsgi')
        run('sudo touch /home/django/djcode/' + prod_deploy_dir + '/dictionary/*.wsgi')





