"""
Created on August 22, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import json
import logging

from aic.aiccore import AICQuery
import aic.common as common

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


class NVPBaseQuery(AICQuery):

    def __init__(self, aic_connection, resource):
        super(NVPBaseQuery, self).__init__(aic_connection, resource)
        logger.info("Created NVPBaseQuery")
        self.query['fields'] = '*'

    def fields(self, fieldlist):
        self.query['fields'] = ','.join(fieldlist)
        return self

    
class NVPEntityQuery(NVPBaseQuery):

    def __init__(self, aic_connection, resource):
        super(NVPEntityQuery, self).__init__(aic_connection, resource)
        logger.info("Created NVPEntityQuery")
        self.query['_page_length'] = 1000

    def page(self, page):
        return self

    def length(self, page):
        self.query['_page_length'] = page
        return self

    def alert(self, flag):
        self.query['alert'] = 'true' if flag else 'false'
        return self

    def alert_changed_since(self, date):
        return self

    def display_name(self, name):
        self.query['display_name'] = name
        return self

    def identifier(self, ident):
        self.query['identifier'] = ident
        return self

    def last_modified(self, date):

        return self

    def tags(self, taglist):
        return self

    def tagscopes(self, tagscopelist):
        return self

    def uuid(self, uid):
        self.query['uuid'] = uid
        return self


class LSwitchQuery(NVPEntityQuery):

    def port_isolation(self, flag):
        self.query['port_isolation'] = 'true' if flag else 'false'
        return self

    def transport_zone_name(self, name):
        self.query['transport_zone_name'] = name
        return self

    def transport_zone_uuid(self, uid):
        self.query['transport_zone_uuid'] = uid
        return self

    def results(self):
        return super(LSwitchQuery, self)._query('GET')

