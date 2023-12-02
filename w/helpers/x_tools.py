#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import hashlib
import datetime
import string
import json

from flask import Response, redirect, url_for
from random import randint, choice


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def extractor(data, key):
    _ = key.split(".")[::-1]
    _key = _.pop()
    if not _key: return data
    if isinstance(data, dict):
        return extractor(data.get(_key), ".".join(_[::-1]))


def redirect_with_error(url, error):
    return redirect(url_for(url, error=error))


def response_create(data, rtype="json", headers=None, response_code=200, cookies=None):
    avail_rsp = {
        "json": "application/json"
    }

    response = Response(
        json.dumps(data, default=json_serial),
        mimetype=avail_rsp[rtype],
        headers=headers,
        status=response_code
    )

    if cookies:
        for c_name, c_value, max_age in cookies:
            response.set_cookie(c_name, c_value, max_age=max_age)

    return response


def random_from_list(source):
    return choice(source)


def strong_password():
    characters = string.ascii_letters + string.digits + "_*!."
    return "".join(choice(characters) for _ in range(randint(8, 16)))


def generate_id():
    return str(uuid.uuid4()).lower().split("-")[-1]


def generate_token():
    return str(uuid.uuid4())


def calculate_hash(target, method="sha256"):
    method_dict = {
        "md5": hashlib.md5,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512
    }
    return method_dict[method](target.encode("utf-8")).hexdigest()


def datetime_pattern(pt=None, dt=None, ct=None, skip_format=False):
    pattern_dict = {
        "ts": "%Y/%m/%d %H:%M:%S",
        "date": "%Y-%m-%d",
        "js": "%Y-%m-%d %H:%M",
        "copyrights": "%Y"
    }
    now = datetime.datetime.utcnow()
    if pt is None:
        pt = "ts"
    if dt is not None:
        if ct is None:
            return dt.strftime(pattern_dict[pt])
        return datetime.datetime.strptime(dt, ct)
    return now.strftime(pattern_dict[pt]) if not skip_format else now


def get_future_date(days):
    return datetime.datetime.now() + datetime.timedelta(days=days)


def calculate_elapsed(time_object, formatted=False):
    if formatted:
        return str((datetime.datetime.now() - time_object))
    return (datetime.datetime.now() - time_object).total_seconds()


def pretty_json(data, indent=4):
    return json.dumps(json.loads(data), indent=indent)


def convert_string_to_bool(stmt):
    return True if stmt in ("True", ) else False
