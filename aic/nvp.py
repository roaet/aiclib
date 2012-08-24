"""
Created on August 23, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import json
import log

import common
import core
import nvpentity

logger = log.get_logger(__name__)



class Connection(core.CoreLib):

    def __init__(self, uri, poolmanager=None, username='admin',
                 password='admin'):
        super(Connection, self).__init__(uri, poolmanager, username, password)

    def nvp_function(self):
        entity = NVPFunction(self)
        return entity

    def lswitch(self, uuid=None):
        uuidvalue = uuid
        if type(uuid) is dict and 'uuid' in uuid:
            uuidvalue = uuid['uuid']
        entity = nvpentity.LSwitch(self, uuid=uuidvalue)
        return entity

    def lswitch_port(self):
        entity = nvpentity.LSwitchPort(self)
        return entity

    def _action(self, entity, method, resource):
        """
        Will inject generation ID into the JSON result object if it exists
        """
        r = super(Connection, self)._action(entity, method, resource)
        logger.info("Response headers: %s" % r.headers)
        responselength = 0
        generationid = None
        if 'x-nvp-config-generation' in r.headers:
            generationid = r.getheader('x-nvp-config-generation')
        if 'content-length' in r.headers:
            responselength = int(r.getheader('content-length'))
        if responselength > 0:
            if r.getheader('content-type') == 'application/json':
                jsonreturn = json.loads(r.data)
                if generationid:
                    jsonreturn['_generationid'] = generationid
                return jsonreturn
            else:
                return r.data
        return


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
