# -*- coding: utf-8 -*-
"""
    eventer.api.shop
    ~~~~~~~~~~~~~~~
    The shop api module.
"""

from flask import abort
from flask_restful import Resource, reqparse, marshal_with, fields

from eventer.api import api, meta_fields
from eventer.models.shop import Shop


shop_parser = reqparse.RequestParser()
shop_parser.add_argument('name')


# Marshaled field definitions for shop objects
shop_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

# Marshaled field definitions for collections of shop objects
shop_collection_fields = {
    'items': fields.List(fields.Nested(shop_fields)),
    'meta': fields.Nested(meta_fields),
}


class ShopResource(Resource):
    """
        Shop api endpoints
    """
    @marshal_with(shop_fields)
    def get(self, shop_id=None, name=None):
        """
            Return shop from id or name
        """
        shop = None
        if name is not None:
            shop = Shop.get_by_name(name)
        else:
            shop = Shop.get_by_id(shop_id)

        if not shop:
            abort(404)

        return shop


class ShopCollectionResource(Resource):
    """
        Shop list api endpoints
    """
    @marshal_with(shop_collection_fields)
    def get(self):
        """
            Get full list of shops
        """
        shops = Shop.query
        return shops


api.add_resource(ShopResource, '/v1/shop/<name>', '/v1/shop/<int:shop_id>')
api.add_resource(ShopCollectionResource, '/v1/shops')

