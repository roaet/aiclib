"""
Created on August 21, 2012

@author: Justin Hammond, Rackspace Hosting
"""
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

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
}


def apimap(method):
    if not method in _apimap:
        raise TypeError('400', "(%s) is an unsupported command" % method)
    uri = "/%s/%s" % (_version, _apimap[method])
    return uri
