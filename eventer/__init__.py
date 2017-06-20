# -*- coding: utf-8 -*-
"""
    eventer
    ~~~~~~~~~~~
    The Flask application module.
"""

import os
from flask import Flask

from eventer.extensions import (
    db,
    migrate,
    crypt,
)
from eventer.api import api_blueprint

if os.getenv('FLASK_ENV') == 'prod':
    config_file = '../config_prod.py'
else:
    config_file = '../config_dev.py'

def create_app(config_filename=config_file):
    '''
        An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

        :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """
        Helper for registering extensions
    """
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """
        Helper for registering blueprints
    """
    app.register_blueprint(api_blueprint)

