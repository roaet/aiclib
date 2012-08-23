"""
Created on August 22, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import logging

import common
import core
import nvpquery

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


class NVPEntity(core.Entity):

    def __init__(self, connection):
        super(NVPEntity, self).__init__(connection)

    def ignore_cluster_majority(self, ignore):
        self.ignore_cluster_majority = ignore
        return self

    def tags(self, tagList):
        #TODO: NVP is inconsistent with the way they handle the multivalued
        #      tag business
        return self

    def display_name(self, name):
        self.info['display_name'] = name
        return self

    def _unroll(self):
        super(NVPEntity, self)._unroll()
        return self.info


class LSwitch(NVPEntity):

    def __init__(self, connection, uuid=None):
        super(LSwitch, self).__init__(connection)
        self.uuid = uuid

    def port_isolation_enabled(self, enabled):
        self.info['port_isolation_enabled'] = enabled
        return self

    def transport_zones(self, zones):
        #TODO: Soon
        return self

    def _unroll(self):
        super(LSwitch, self)._unroll()
        return self.info

    def query(self):
        queryobject = nvpquery.LSwitchQuery(self.connection,
                                            common.apimap('lswitch'))
        return queryobject

    def create(self):
        return super(LSwitch, self)._action('POST', common.apimap('lswitch'))

    def delete(self):
        if not self.uuid:
            logger.error("Attempted to delete without UUID: failing")
            return None
        uri = "%s/%s" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('DELETE', uri)

    def status(self):
        if not self.uuid:
            logger.error("Attempted to check status without UUID: failing")
            return None
        uri = "%s/%s/status" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('GET', uri)

    def read(self):
        if not self.uuid:
            logger.error("Attempted to read config without UUID: failing")
            return None
        uri = "%s/%s" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('GET', uri)

    def update(self):
        if not self.uuid:
            logger.error("Attempted to update config without UUID: failing")
            return None
        uri = "%s/%s" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('PUT', uri)


class LSwitchPort(NVPEntity):

    def __init___(self, connection):
        super(LSwitchPort, self).__init__(connection)

    def admin_status_enabled(self, enabled):
        self.info['admin_status_enabled'] = enabled
        return self

    def _unroll(self):
        super(LSwitchPort, self)._unroll()
        return self.info
