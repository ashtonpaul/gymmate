from __future__ import with_statement

import logging

from fabric.api import run, sudo
from fabric.api import env
from fabric.network import disconnect_all
from fabric.context_managers import cd

logging.getLogger('paramiko.transport').addHandler(logging.StreamHandler())

code_path = "~/www/html"

env.hosts = ["staging.dnsdynamic.com"]
env.user = "pi"
env.password = "fuckdying1"


def deploy(project_name=None):
    sudo("apt-get install -y libmysqlclient-dev")
    with cd(code_path):
        run("rm -rf {0}_env".format(project_name))
        run("rm -rf {0}".format(project_name))
        run("virtualenv {0}_env".format(project_name))
        run("source {0}_env/bin/activate".format(project_name))
        run("git clone -b develop git@bitbucket.org:ashtonpaul/{0}.git".format(project_name))
        run("{0}_env/bin/pip install -r {0}/requirements.txt".format(project_name))
        run("python {0}/manage.py migrate".format(project_name))
        run("python {0}/manage.py collectstatic --no-input".format(project_name))
        disconnect_all()
