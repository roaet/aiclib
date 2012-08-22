"""
Created on August 22, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import json
import logging

import aic.common as common

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


class AICEntity(object):

    def __init__(self, aic_connection):
        logger.info("Created AICEntity")
        self.aic_connection = aic_connection
        self.info = {}

    def _action(self, method, resource):
        return self.aic_connection._action(self, method, resource)

    def _unroll(self):
        return self.info


class AICQuery(object):

    def __init__(self, aic_connection, resource):
        logger.info("Created AICQuery")
        self.aic_connection = aic_connection
        self.query = {}
        self.resource = resource

    def _query(self, method):
        return self.aic_connection._action(self, method, self.resource)

    def _unroll(self):
        return self.query

