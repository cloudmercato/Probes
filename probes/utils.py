"""Utilities for probes"""
import datetime
import json


class ProbesError(Exception):
    """Base Exception for all probes' error"""


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
