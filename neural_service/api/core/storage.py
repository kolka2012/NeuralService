# -*- coding: utf-8 -*-

from __future__ import absolute_import

from werkzeug.exceptions import BadRequest


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
                filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))