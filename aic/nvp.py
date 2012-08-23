"""
Created on August 23, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import logging

import common
import core
import nvpentity

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
        entity = NVPFunction(self)
        return entity

    def lswitch(self, uuid=None):
        entity = nvpentity.LSwitch(self, uuid=uuid)
        return entity

    def lswitch_port(self):
        entity = nvpentity.LSwitchPort(self)
        return entity


class NVPFunction(core.Entity):

    def __init__(self, connection):
        super(NVPFunction, self).__init__(connection)

    def logout(self):
        return super(NVPFunction, self)._action(
                'GET', common.apimap('logout'))

    def get_method_uris(self):
        return super(NVPFunction, self)._action(
                'GET', common.apimap('getMethodURIs'))

    def read_method(self, method_name):
        uri = "%s/%s" % (common.apimap('readMethod'), method_name)
        return super(NVPFunction, self)._action('GET', uri)

    def get_schemas(self):
        return super(NVPFunction, self)._action(
                'GET', common.apimap('schema'))

    def read_schema(self, schema_name):
        uri = "%s/%s" % (common.apimap('readSchema'), schema_name)
        return super(NVPFunction, self)._action('GET', uri)
