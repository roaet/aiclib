"""
Created on August 21, 2012

@author: Justin Hammond, Rackspace Hosting
"""
import calendar
import log
import re


logger = log.get_logger(__name__)

_version = 'ws.v1'


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
