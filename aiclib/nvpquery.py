"""
Created on August 22, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import log

import common
import core

logger = log.get_logger(__name__)


class NVPBaseQuery(core.Query):

    def __init__(self, aic_connection, resource):
        super(NVPBaseQuery, self).__init__(aic_connection, resource)
        logger.info("Created NVPBaseQuery")
        self.query['fields'] = '*'

    def fields(self, fieldlist):
        if isinstance(fieldlist, str):
            fieldlist = [fieldlist]
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

    def alert_changed_since(self, comparison, date_time):
        """Comparison operator (string): >,>=,<,<=,=,!=
        """
        query_value = "%s%s" % (comparison, common.dttounix(date_time))
        self.query['alert_changed_since'] = query_value
        return self

    def display_name(self, name):
        self.query['display_name'] = name
        return self

    def identifier(self, ident):
        self.query['identifier'] = ident
        return self

    def last_modified(self, comparison, date_time):
        """Comparison operator (string): >,>=,<,<=,=,!=
        """
        query_value = "%s%s" % (comparison, common.dttounix(date_time))
        self.query['last_modified'] = query_value
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


class QOSQueueQuery(NVPEntityQuery):
    #TODO: Add all entity specific features

    def results(self):
        return super(QOSQueueQuery, self).results()


class SecurityProfileQuery(NVPEntityQuery):
    #TODO: Add all entity specific features

    def results(self):
        return super(SecurityProfileQuery, self).results()


class LRouterQuery(NVPEntityQuery):
    #TODO: Add all entity specific features

    def results(self):
        return super(LRouterQuery, self).results()


class TransportNodeQuery(NVPEntityQuery):
    #TODO: Add all entity specific features

    def results(self):
        return super(TransportNodeQuery, self).results()


class MDIServiceQuery(NVPEntityQuery):
    #TODO: Add all entity specific features

    def results(self):
        return super(MDIServiceQuery, self).results()


class TransportZoneQuery(NVPEntityQuery):
    #TODO: Add all entity specific features

    def results(self):
        return super(TransportZoneQuery, self).results()


class GatewayServiceQuery(NVPEntityQuery):
    #TODO: Add all entity specific features

    def results(self):
        return super(GatewayServiceQuery, self).results()


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
