# -*- coding: utf-8 -*-
"""
    eventer.models.shop
    ~~~~~~~~~~~~~~~
    The Shop model.
"""

from eventer.database import (
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


class Shop(SurrogatePK, Model):
    """
        Shop definition
    """
    __tablename__ = 'shops'

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')

    name = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False, server_default='')
    phone1 = db.Column(db.String(15), nullable=False, server_default='')
    phone2 = db.Column(db.String(15), nullable=False, server_default='')
    email = db.Column(db.String(255), nullable=False, server_default='')

    subway = db.Column(db.String(255), nullable=False, server_default='')
    tram = db.Column(db.String(255), nullable=False, server_default='')
    bus = db.Column(db.String(255), nullable=False, server_default='')
    trolley = db.Column(db.String(255), nullable=False, server_default='')

    latitude = db.Column(db.Float, nullable=False, server_default='0')
    longitude = db.Column(db.Float, nullable=False, server_default='0')

    # opening_hours = db.Column(JSON, nullable=False, server_default='')
    opening_hours = db.Column(db.String(1024), nullable=False, server_default='')
    picture = db.Column(db.String(255), nullable=False, server_default='')

    # Activity information
    created_on = db.Column(db.DateTime(), nullable=False)
    # confirmed_at = db.Column(DateTime())

    # Relationships with other tables
    user_id = ReferenceCol('users')
    users = relationship('User', back_populates='shops')
    events = relationship('Event', back_populates='shop')

    def get_id(self):
        """
            return self id
        """
        return self.__id

    @classmethod
    def get_by_name(cls, name):
        """
            Return the full shop from the name
        """
        return cls.query.filter_by(name=name).first()


# TODO:
# class ShopLog(Model):
#     """
#         Shop log
#     """
#     __tablename__ = 'shop_log'
#
#     __id = db.Column('id', Integer, primary_key=True)
#
#     shop = relationship('Shop', back_populates='log')
