"""
Created on August 22, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import logging

import core

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


class NVPBaseQuery(core.Query):

    def __init__(self, aic_connection, resource):
        super(NVPBaseQuery, self).__init__(aic_connection, resource)
        logger.info("Created NVPBaseQuery")
        self.query['fields'] = '*'

    def fields(self, fieldlist):
        self.query['fields'] = ','.join(fieldlist)
        return self

    def results(self):
        results = super(NVPEntityQuery, self)._query('GET')
        return results


class NVPEntityQuery(NVPBaseQuery):

    def __init__(self, aic_connection, resource):
        super(NVPEntityQuery, self).__init__(aic_connection, resource)
        logger.info("Created NVPEntityQuery")
        self.query['_page_length'] = 1000
        self.nextpage = None

    def length(self, page):
        self.query['_page_length'] = page
        return self

    def alert(self, flag):
        self.query['alert'] = 'true' if flag else 'false'
        return self

    def alert_changed_since(self, date):
        #TODO: Need to figure out what date format NVP wants
        return self

    def display_name(self, name):
        self.query['display_name'] = name
        return self

    def identifier(self, ident):
        self.query['identifier'] = ident
        return self

    def last_modified(self, date):
        #TODO: Need to figure out what date format NVP wants
        return self

    def tags(self, taglist):
        #TODO: NVP treats taglists differently and this requires thought
        return self

    def tagscopes(self, tagscopelist):
        #TODO: Will do with tags
        return self

    def uuid(self, uid):
        self.query['uuid'] = uid
        return self

    def next(self):
        if not self.nextpage:
            return None
        self.query['_page_cursor'] = self.nextpage
        return self.results()

    def results(self):
        results = super(NVPEntityQuery, self).results()
        if type(results) is dict and 'page_cursor' in results:
            self.nextpage = results['page_cursor']
        else:
            self.nextpage = None
        return results


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
        #TODO: This may require some modifications at this level
        return super(LSwitchQuery, self).results()
