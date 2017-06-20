# -*- coding: utf-8 -*-
"""
    eventer.api.event
    ~~~~~~~~~~~~~~~
    The event api module.
"""

from flask import abort
from flask_restful import Resource, reqparse, marshal_with, fields

from eventer.api import api, meta_fields
from eventer.models.event import Event


event_parser = reqparse.RequestParser()
event_parser.add_argument('name')


# Marshaled field definitions for event objects
event_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

# Marshaled field definitions for collections of event objects
event_collection_fields = {
    'items': fields.List(fields.Nested(event_fields)),
    'meta': fields.Nested(meta_fields),
}


class EventResource(Resource):
    """
        Event api endpoints
    """
    @marshal_with(event_fields)
    def get(self, event_id=None, name=None):
        """
            Return event from id or name
        """
        event = None
        if name is not None:
            event = Event.get_by_name(name)
        else:
            event = Event.get_by_id(event_id)

        if not event:
            abort(404)

        return event


class EventCollectionResource(Resource):
    """
        Event list api endpoints
    """
    @marshal_with(event_collection_fields)
    def get(self):
        """
            Get full list of events
        """
        events = Event.query
        return events


api.add_resource(EventResource, '/v1/event/<name>', '/v1/event/<int:event_id>')
api.add_resource(EventCollectionResource, '/v1/events')

