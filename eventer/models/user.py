# -*- coding: utf-8 -*-
"""
    eventer.models.user
    ~~~~~~~~~~~~~~~
    The User model.
"""

from datetime import datetime, timedelta
import uuid
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)

from eventer.database import (
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)
from eventer.extensions import crypt


class User(SurrogatePK, Model):
    """
        User definition
    """
    __tablename__ = 'users'

    active = db.Column(db.Boolean(), nullable=False, server_default='1')

    # User authentication information
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # User information
    name = db.Column(db.String(255), nullable=False, server_default='')
    admin = db.Column(db.Boolean(), nullable=False, server_default='0')

    # Activity information
    created_on = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    # confirmed_at = Column(DateTime())

    # Relationships with other tables
    tokens = relationship('UserToken', back_populates='user')
    shops = relationship('Shop', back_populates='users')

    def __init__(self, username, password, **kwargs):
        db.Model.__init__(self, username=username, password=password, **kwargs)
        self.set_password(password)

    @property
    def password(self):
        """
            Bogus password property
        """
        return None

    @property
    def is_admin(self):
        """
            Check if the user has the admin flag set
        """
        return self.admin

    @password.setter
    def password(self, password):
        self.set_password(password)

    def set_password(self, password):
        """
            Generate password hash form plain text password
        """
        self.password_hash = crypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, value):
        """
            Check a plain text password against the password hash
        """
        return crypt.check_password_hash(self.password_hash, value)

    @classmethod
    def get_by_username(cls, username):
        """
            Return the full user from the username
        """
        return cls.query.filter_by(username=username).first()

    def generate_auth_token(self, expiration=600):
        """
            Generate the authorization token
        """
        # TODO: token = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        token = Serializer('SECRET_KEY', expires_in=expiration)
        return token.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
            Verify if the authorization token is valid
        """
        stored_token = Serializer('SECRET_KEY')
        try:
            data = stored_token.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)


class UserToken(SurrogatePK, Model):
    """
        Login tokens
    """
    __tablename__ = 'user_tokens'

    token = db.Column(db.String(36), nullable=False)
    registered_on = db.Column(db.DateTime(), nullable=False)
    expires_on = db.Column(db.DateTime(), nullable=False)

    # Relationships with other tables
    user_id = ReferenceCol('users')
    shop_id = ReferenceCol('shops')
    user = relationship('User', back_populates='tokens')

    def __init__(self, user_id):
        self.token = uuid.uuid4()
        self.registered_on = datetime.now()
        # self.expires_on = datetime.now() + timedelta(seconds=app.config.get('TOKEN_VALIDITY'))
        # TODO: change with app.config
        self.expires_on = datetime.now() + timedelta(seconds=86400)
        self.user_id = user_id

    @property
    def is_valid(self):
        """
            Checks if the current token is still valid
        """
        if self.expires_on < datetime.now():
            return True
        return False


# TODO:
# class UserActivity(Model):
#     """
#         User activity
#     """
#     __tablename__ = 'user_activity'
#
#     __id = Column('id', Integer, primary_key=True)
#
#     user = relationship('User', back_populates='activity')


# TODO:
# class UserLog(Model):
#     """
#         User log
#     """
#     __tablename__ = 'user_log'
#
#     __id = Column('id', Integer, primary_key=True)
#
#     user = relationship('User', back_populates='log')
