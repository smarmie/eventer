#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    eventer.utils
    ~~~~~
    Utility methods.
    I'm including this file in the skeleton because it contains methods I've
    found useful.

    The goal is to keep this file as lean as possible.

"""
from flask import request
# import app


def prepare_json_response(success, message, data):
    """
        Create a json file with the response
    """
    response = {"meta":{"success":success, "request":request.url}}
    if data:
        response["data"] = data
        response["meta"]["data_count"] = len(data)

    if message:
        response["meta"]["message"] = message

    return response

