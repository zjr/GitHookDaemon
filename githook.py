#!/usr/bin/env python2.7

import os
import web
import json
import urlparse

from subprocess import check_call

urls = ('/.*', 'Hooks')
app = web.application(urls, globals())


def OwnSet(user, loc):
    check_call([
        'chown',
        '-R',
        user + ':' + user,
        loc
    ])


def PermSet(loc):
    for dirpath, dirnames, filenames in os.walk(loc):
        os.chmod(dirpath, 0o755)
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            os.chmod(path, 0o644)


class Hooks:
    def POST(self):
        r = web.data()
        data = urlparse.parse_qs(r)
        dataJ = json.loads(data['payload'][0])
        if (dataJ['repository']['name'] == 'commer' and
                dataJ['ref'] == 'refs/heads/master'):
            os.chdir('/home/commer/')
            check_call([
                'git',
                'pull'
            ])
            check_call([
                'grunt',
                'build'
            ])
            OwnSet('commer', 'public_html_o')
            check_call([
                'rm',
                '-rf',
                'public_html'
            ])
            check_call([
                'mv',
                'public_html_o',
                'public_html'
            ])
            PermSet('public_html')
            os.chdir('/')
        elif (dataJ['repository']['name'] == 'acclmd-site' and
                dataJ['ref'] == 'refs/heads/master'):
            os.chdir('/home/acclaim/public_html/live')
            os.environ['GIT_DIR'] = '../live.git'
            check_call([
                'git',
                'pull'
            ])
            del os.environ['GIT_DIR']
            OwnSet('acclaim', '.')
            PermSet('.')
            os.chmod('nearby.py', 0o755)
            os.chdir('/')
        elif (dataJ['repository']['name'] == 'lompoc' and
                dataJ['ref'] == 'refs/heads/master'):
            os.chdir('/home/lompoc/public_html')
            os.environ['GIT_DIR'] = '../repo'
            os.environ['GIT_WORK_TREE'] = '.'
            check_call([
                'git',
                'pull'
            ])
            del os.env['GIT_DIR']
            del os.env['GIT_WORK_TREE']
            OwnSet('lompoc', '.')
            PermSet('.')
            os.chdir('/')

if __name__ == '__main__':
    app.run()
