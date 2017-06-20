# -*- coding: utf-8 -*-
"""
    eventer.api.user
    ~~~~~~~~~~~~~~~
    The user api module.
"""

from flask import abort, g
from flask_restful import Resource, reqparse, marshal_with, fields

from eventer.api import api, meta_fields
from eventer.api.auth import self_only, admin_only
from eventer.models.user import User
from eventer.extensions import auth


user_parser = reqparse.RequestParser()
user_parser.add_argument('username')
user_parser.add_argument('password')
user_parser.add_argument('name')


# Marshaled field definitions for user objects
user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String,
}

# Marshaled field definitions for collections of user objects
user_collection_fields = {
    'items': fields.List(fields.Nested(user_fields)),
    'meta': fields.Nested(meta_fields),
}


class UserResource(Resource):
    """
        User api endpoints
    """
    @auth.login_required
    @marshal_with(user_fields)
    def get(self, user_id=None, username=None):
        """
            Return user from id or username
        """
        if username is not None:
            user = User.get_by_username(username)
        else:
            user = User.get_by_id(user_id)
        if not user:
            abort(404)
        return user

    @auth.login_required
    @self_only
    @marshal_with(user_fields)
    def post(self, user_id=None, username=None):
        """
            Update current user
        """
        g.user.update(**user_parser.parse_args())
        return g.user

    @auth.login_required
    @admin_only
    def delete(self, user_id=None, username=None):
        """
            Delete a user.
            Must be admin.
        """
        g.user.delete()
        return 204


class UserCollectionResource(Resource):
    """
        User list api endpoints
    """
    @marshal_with(user_collection_fields)
    @auth.login_required
    def get(self):
        """
            Get full list of users
        """
        users = User.query
        return users

    @auth.login_required
    @admin_only
    @marshal_with(user_fields)
    def post(self):
        """
            Create multiple users
        """
        user = User.create(**user_parser.parse_args())
        return user, 201


api.add_resource(UserResource, '/v1/user/<username>', '/v1/user/<int:user_id>')
api.add_resource(UserCollectionResource, '/v1/users')
