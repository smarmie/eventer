# -*- coding: utf-8 -*-
"""
    eventer.controllers
    ~~~~~~~~~~~~~~~
    The controllers module.
"""

from flask import Blueprint
from flask_restful import Api, fields

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)

# Marshaled fields for links in meta section
link_fields = {
    'prev': fields.String,
    'next': fields.String,
    'first': fields.String,
    'last': fields.String,
}

# Marshaled fields for meta section
meta_fields = {
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total': fields.Integer,
    'pages': fields.Integer,
    'links': fields.Nested(link_fields)
}

# Import the resources to add the routes to the blueprint before the app is
# initialized
from . import user
from . import shop
from . import event
