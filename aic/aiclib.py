"""
Created on August 17, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import json
import logging

import urllib3

import common
from aic.aiclibconnection import AICLibConnection
import aic.nvpentity as nvpentity
import aic.nvpquery as nvpquery

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
            self.conn = urllib3.connection_from_url(uri)
        else:
            self.conn = poolManager.connection_from_url(uri)
        self.connection = AICLibConnection(connection=self.conn,
                                           username=username,
                                           password=password)

    def identity(self):
        return self

    def nvp_function(self):
        aic_entity = nvpentity.NVPFunction(self)
        return aic_entity

    def lswitch(self, uuid=None):
        aic_entity = nvpentity.LSwitch(self, uuid=uuid)
        return aic_entity

    def lswitch_port(self):
        aic_entity = nvpentity.LSwitchPort(self)
        return aic_entity

    def _action(self, aic_entity, method, resource):
        if not aic_entity:
            return
        logger.info("(%s @ %s): %s" % (method, resource, 
                                       aic_entity._unroll()))
        r = self.connection.request(method, resource,
                                          body = aic_entity._unroll())
        logger.info("Response headers: %s" % r.headers)
        responseLength = 0
        if 'content-length' in r.headers:
            responseLength = int(r.getheader('content-length'))
        if responseLength > 0:
            if r.getheader('content-type') == 'application/json':
                jsonReturn = json.loads(r.data)
                return jsonReturn
            else:
                return r.data
        return None


