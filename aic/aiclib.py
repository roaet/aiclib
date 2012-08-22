'''
Created on August 17, 2012

@author: Justin Hammond, Rackspace Hosting
'''

import json
import logging

import urllib3

import common
from aic.aiclibconnection import AICLibConnection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


class AICLib(object):


    def __init__(self, uri, poolManager=None, username='admin', 
                 password='admin'):
        '''
        Constructor for the AICLib object.
        - If pool_manager is 
        '''
        if poolManager is None:
            #TODO: config this constant
            self.conn = urllib3.connection_from_url(uri)
        else:
            self.conn = poolManager.connection_from_url(uri)
        self.connection = AICLibConnection(connection=self.conn,
                                           username=username,
                                           password=password)
       

    def identity(self):
        return self


    def nvp_function(self):
        aic_entity = NVPFunction(self)
        return aic_entity


    def lswitch(self):
        aic_entity = LSwitch(self)
        return aic_entity


    def lswitch_port(self):
        aic_entity = LSwitchPort(self)
        return aic_entity


    def _action(self, aic_entity, method, resource):
        if not aic_entity:
            return
        logger.info("(%s @ %s): %s" % (method, resource, 
                                       aic_entity._unroll()))
        r = self.connection.request(method, resource,
                                          body = aic_entity._unroll())
        if r.getheader('content-length') > 0:
            if r.getheader('content-type') == 'application/json':
                jsonReturn = json.loads(r.data)
                return jsonReturn
            else:
                return r.data
        return None



class AICEntity(object):
    

    def __init__(self, aic_connection):
        logger.info("Created AICEntity")
        self.aic_connection = aic_connection
        self.info = {}

    def _action(self, method, resource):
        return self.aic_connection._action(self, method, resource)


    def _unroll(self):
        return self.info


class NVPFunction(AICEntity):


    def __init__(self, aic_connection):
        super(NVPFunction, self).__init__(aic_connection)
        logger.info("Created NVPFunction")


    def logout(self):
        return super(NVPFunction, self)._action('GET', common.apimap('logout'))


    def get_method_uris(self):
        return super(NVPFunction, self)._action('GET', 
                                                common.apimap('getMethodURIs'))


    def read_method(self, method_name):
        uri = "%s/%s" % (common.apimap('readMethod'), method_name)
        return super(NVPFunction, self)._action('GET', uri)


    def get_schemas(self):
        return super(NVPFunction, self)._action('GET', common.apimap('schema'))


    def read_schema(self, schema_name):
        uri = "%s/%s" % (common.apimap('readSchema'), schema_name)
        return super(NVPFunction, self)._action('GET', uri)


class NVPEntity(AICEntity):


    def __init__(self, aic_connection):
        super(NVPEntity, self).__init__(aic_connection)
        logger.info("Created NVPEntity")


    def ignore_cluster_majority(ignore):
        self.ignore_cluster_majority = ignore
        return self


    def tags(self, tagList):
        logger.info("Messing with tags")
        return self


    def display_name(self, name):
        self.info['display_name'] = name
        return self


    def _unroll(self):
        super(NVPEntity, self)._unroll()
        return self.info


class LSwitch(NVPEntity):


    def __init__(self, aic_connection):
        super(LSwitch, self).__init__(aic_connection)


    def port_isolation_enabled(self, enabled):
        self.info['port_isolation_enabled'] = enabled
        return self


    def transport_zones(self, zones):
        return self


    def _unroll(self):
        super(LSwitch, self)._unroll()
        return self.info


    def create(self):
        return super(LSwitch, self)._action('POST', common.apimap('lswitch'))


class LSwitchPort(NVPEntity):


    def __init___(self, aic_connection):
        super(LSwitchPort, self).__init__(aic_connection)


    def admin_status_enabled(self, enabled):
        self.info['admin_status_enabled'] = enabled
        return self


    def _unroll(self):
        super(LSwitchPort, self)._unroll()
        return self.info



