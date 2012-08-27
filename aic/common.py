"""
Created on August 21, 2012

@author: Justin Hammond, Rackspace Hosting
"""
import calendar
import log


logger = log.get_logger(__name__)

_version = 'ws.v1'

#TODO: Needs to be changed to something less bad
_apimap = {
    'login': 'login',
    'logout': 'logout',
    'schema': 'schema',
    'readMethod': 'doc/method',
    'readSchema': 'schema',
    'getMethodURIs': 'doc/method',
    'manual': 'doc/reference',
    'controlCluster': 'control-cluster',
    # switch commands
    'lswitch': 'lswitch',
    'lport': 'lport',
}


def apimap(method):
    if not method in _apimap:
        raise TypeError('400', "(%s) is an unsupported command" % method)
    uri = "/%s/%s" % (_version, _apimap[method])
    return uri


def dttounix(date_time):
    unixtime = calendar.timegm(date_time.utctimetuple())
    return unixtime
