# -*- coding: utf-8 -*-
"""
    eventer.api.auth
    ~~~~~~~~~~~~~~~
    The authentication api module.
"""

import functools
from flask import g, abort, jsonify
from flask_restful import Resource

from eventer.api import api
from eventer.extensions import auth
from eventer.models.user import User


class AuthGetToken(Resource):
    """
        Get authorization token
    """
    @auth.login_required
    def get(self):
        """
            Return event from id or name
        """
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    """
        Validate user passwords and store user in the 'g' object
    """
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def self_only(func):
    """
        Ensure that the user making the request is the current user
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get('username', None):
            if g.user.username != kwargs['username']:
                abort(403)
        if kwargs.get('user_id', None):
            if g.user.id != kwargs['user_id']:
                abort(403)
        return func(*args, **kwargs)
    return wrapper


def admin_only(func):
    """
        Ensure that the user making the request is an administrator
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return wrapper


api.add_resource(AuthGetToken, '/v1/auth/token')
