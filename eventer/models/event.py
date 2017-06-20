# -*- coding: utf-8 -*-
"""
    eventer.models.event
    ~~~~~~~~~~~~~~~
    The Event model.
"""

from eventer.database import (
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


class Event(SurrogatePK, Model):
    """
        Event definition
    """
    __tablename__ = 'events'

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')

    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False, server_default='')
    start = db.Column(db.DateTime(), nullable=False)
    end = db.Column(db.DateTime(), nullable=False)

    # Activity information
    created_on = db.Column(db.DateTime(), nullable=False)

    # Relationships with other tables
    shop_id = ReferenceCol('shops')
    shop = relationship('Shop', back_populates='events')

    def get_id(self):
        """
            return self id
        """
        return self.__id

    @classmethod
    def get_by_name(cls, name):
        """
            Return the full event from the name
        """
        return cls.query.filter_by(name=name).first()


# TODO:
# class EventLog(Model):
#     """
#         Event log
#     """
#     __tablename__ = 'event_log'
#
#     __id = db.Column('id', Integer, primary_key=True)
#
#     event = relationship('Event', back_populates='event')
