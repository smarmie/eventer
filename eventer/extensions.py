# -*- coding: utf-8 -*-
"""
    eventer.extensions
    Extensions module. Each extension is initialized in the app factory located
    in __init__.py
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth


db = SQLAlchemy()
migrate = Migrate()
crypt = Bcrypt()
auth = HTTPBasicAuth()
