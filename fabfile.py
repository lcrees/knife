'''knife fabfile'''

from fabric.api import prompt, local, settings, env, lcd


def _test(val):
    truth = val in ['py26', 'py27', 'py31', 'py32']
    if truth is False:
        raise KeyError(val)
    return val


def tox():
    '''test knife'''
    local('tox')


def docs():
    with lcd('./docs/'):
        local('make clean')
        local('make html')
        local('make linkcheck')
        local('make doctest')


def update_docs():
    docs()
    local('hg ci -m docmerge; hg push')
    local('./setup.py upload_sphinx')


def tox_recreate():
    '''recreate knife test env'''
    prompt(
        'Enter testenv: [py26, py27, py31, py32]',
        'testenv',
        validate=_test,
    )
    local('tox --recreate -e %(testenv)s' % env)


def release():
    '''release knife'''
    local('hg update pu')
    local('hg update next')
    local('hg merge pu; hg ci -m automerge')
    local('hg update maint')
    local('hg merge default; hg ci -m automerge')
    local('hg update default')
    local('hg merge next; hg ci -m automerge')
    local('hg update pu')
    local('hg merge default; hg ci -m automerge')
    prompt('Enter tag: ', 'tag')
    with settings(warn_only=True):
        local('hg tag "%(tag)s"' % env)
        local('hg push ssh://hg@bitbucket.org/lcrees/knife')
        local('hg push git+ssh://git@github.com:kwarterthieves/knife.git')
    local('./setup.py register sdist --format=bztar,gztar,zip upload')
    local('./setup.py upload_sphinx')
    local('rm -rf dist')


def inplace():
    '''inplace knife'''
    with settings(warn_only=True):
        local('hg push ssh://hg@bitbucket.org/lcrees/knife')
        local('hg push git+ssh://git@github.com:kwarterthieves/knife.git')
    local('./setup.py sdist --format=bztar,gztar,zip upload')
    update_docs()
    local('rm -rf dist')


def release_next():
    '''release knife from next branch'''
    local('hg update maint')
    local('hg merge default; hg ci -m automerge')
    local('hg update default')
    local('hg merge next; hg ci -m automerge')
    local('hg update next')
    local('hg merge default; hg ci -m automerge')
    prompt('Enter tag: ', 'tag')
    with settings(warn_only=True):
        local('hg tag "%(tag)s"' % env)
        local('hg push ssh://hg@bitbucket.org/lcrees/knife')
        local('hg push git+ssh://git@github.com:kwarterthieves/knife.git')
    local('./setup.py register sdist --format=bztar,gztar,zip upload')
    local('rm -rf dist')
