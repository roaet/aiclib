"""
Created on August 23, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import json
import logging

import common
import core
import nvpentity
import nvpquery

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


class Connection(core.CoreLib):

    def __init__(self, uri, poolmanager=None, username='admin',
                 password='admin'):
        super(Connection, self).__init__(uri, poolmanager, username, password)

    def nvp_function(self):
        entity = _NVPFunction(self)
        return entity

    def lswitch(self, uuid=None):
        entity = nvpentity._LSwitch(self, uuid=uuid)
        return entity

    def lswitch_port(self):
        entity = nvpentity._LSwitchPort(self)
        return entity


class _NVPFunction(core.Entity):

    def __init__(self, connection):
        super(NVPFunction, self).__init__(connection)

    def logout(self):
        return super(_NVPFunction, self)._action(
                'GET', common.apimap('logout'))

    def get_method_uris(self):
        return super(_NVPFunction, self)._action(
                'GET', common.apimap('getMethodURIs'))

    def read_method(self, method_name):
        uri = "%s/%s" % (common.apimap('readMethod'), method_name)
        return super(_NVPFunction, self)._action('GET', uri)

    def get_schemas(self):
        return super(_NVPFunction, self)._action(
                'GET', common.apimap('schema'))

    def read_schema(self, schema_name):
        uri = "%s/%s" % (common.apimap('readSchema'), schema_name)
        return super(_NVPFunction, self)._action('GET', uri)

