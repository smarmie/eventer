# -*- coding: utf-8 -*-
"""
    This file starts the WSGI web application.
    Usage examples:
    python manage.py help
"""

from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand
from getpass import getpass

from eventer import create_app
from eventer.models.user import User
from eventer.database import db

app = create_app()
manager = Manager(app)


def _make_context():
    """
        Return context dict for a shell session so you can access
        app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test():
    """
        Run the tests.
    """
    import pytest
    exit_code = pytest.main(['tests', '-q'])
    return exit_code


@manager.command
def init():
    """
        Initialize the database.
        Amongst other things, create the admin user
    """
    username = raw_input('Enter admin username: ')
    password = getpass('Input password for the {} user: '.format(username))
    user = User.create(username=username,
                       password=password,
                       admin=True,
                       active=True)
    return user


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
