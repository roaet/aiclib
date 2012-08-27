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


def grab_uuid_of_type(text_or_dict, nvptype):
    if not type(text_or_dict) is dict:
        return text_or_dict
    errormsg = "Missing key (%s) from dictionary when expected."
    typeerror = "Incorrect type (%s); expected %s"
    if not 'uuid' in text_or_dict:
        log.logging.error(errormsg % "uuid")
        raise TypeError(errormsg % "uuid")
    if not 'type' in text_or_dict:
        log.logging.error(errormsg % "type")
        raise TypeError(errormsg % "type")
        if text_or_dict['type'] != nvptype:
            log.logging.error(typeerror % (text_or_dict['type'], nvptype))
            raise TypeError(typeerror % (text_or_dict['type'], nvptype))
    return text_or_dict['uuid']


class Connection(core.CoreLib):

    def __init__(self, uri, poolmanager=None, username='admin',
                 password='admin'):
        super(Connection, self).__init__(uri, poolmanager, username, password)

    def nvp_function(self):
        entity = NVPFunction(self)
        return entity

    def lswitch(self, uuid=None):
        uuidvalue = grab_uuid_of_type(uuid, "LogicalSwitchConfig")
        entity = nvpentity.LSwitch(self, uuid=uuidvalue)
        return entity

    def lswitch_port(self, lswitch_uuid, uuid=None):
        """Will create an Logical Switch port on the passed Logical switch
        or passed UUID of a Logical switch"""
        lswitch_uuid_value = grab_uuid_of_type(lswitch_uuid,
                                               "LogicalSwitchConfig")
        lport_uuid_value = grab_uuid_of_type(uuid,
                                             "LogicalSwitchPortConfig")
        entity = nvpentity.LSwitchPort(self, lswitch_uuid_value,
                                       lport_uuid_value)
        return entity

    def _action(self, entity, method, resource):
        """Will inject generation ID into the JSON result object if it exists
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
