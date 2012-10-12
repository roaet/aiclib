"""
Created on August 21, 2012

@author: Justin Hammond, Rackspace Hosting
"""
import calendar
import logging
import re


logger = logging.getLogger(__name__)

_version = 'ws.v1'
stringoperators = ['=', '!=', '~', '!~']
booleanoperators = ['=', '!=', '<', '>', '<=', '>=']


def is_stringop(stringop):
    return stringop in stringoperators


def is_booleanop(boolop):
    return boolop in booleanoperators


def genuri(*args):
    uri = "/%s/%s" % (_version, "/".join(args))
    return uri


def dttounix(date_time):
    unixtime = calendar.timegm(date_time.utctimetuple())
    return unixtime


def isuuid(uuid):
    regex = "%s-%s-%s-%s-%s" % ("[a-f0-9]{8}", "[a-f0-9]{4}",
                                "[a-f0-9]{4}", "[a-f0-9]{4}",
                                "[a-f0-9]{12}")
    return re.match(regex, uuid)
