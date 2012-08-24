"""
Created on August 22, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import log

import common
import core
import nvpquery

logger = log.get_logger(__name__)


def requireuuid(fn):
    def wrapper(self):
        if not self.uuid:
            msg = "Missing UUID for verb (%s). Failing"
            logger.error(msg % fn.__name__)
            return None
        return fn(self)
    return wrapper


class NVPEntity(core.Entity):

    def __init__(self, connection):
        super(NVPEntity, self).__init__(connection)

    def ignore_cluster_majority(self, ignore):
        self.ignore_cluster_majority = ignore
        return self

    def tags(self, taglist):
        """
        Will set/update the tag list of the object.

        This function is expecting a list of dictionaries that each have,
        at most, two values:
        {
            'tag':<some value>,
            'scope':<some value>
        }

        If a list is not given and only a dictionary is given it will put the
        dictionary in a list for you.

        In all situations the tag element is required.
        """
        if not type(taglist) is list:
            taglist = [taglist]
        self.info['tags'] = taglist
        return self

    def display_name(self, name):
        """
        Will set/update the display name of the object. By default if a
        display name is not given the generated UUID will be used as the
        display name.
        """
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
        """
        Will set/update the port_isolation_enabled flag on the switch
        """
        self.info['port_isolation_enabled'] = enabled
        return self

    def transport_zones(self, zones):
        """
        Will set/update the transport zones that the switch is a 'member' of
        """
        #TODO: Soon
        return self

    def _unroll(self):
        super(LSwitch, self)._unroll()
        return self.info

    def query(self):
        """
        Returns the query object for logical switches
        """
        queryobject = nvpquery.LSwitchQuery(self.connection,
                                            common.apimap('lswitch'))
        return queryobject

    def create(self):
        """
        Create (verb) will create the logical switch
        """
        return super(LSwitch, self)._action('POST', common.apimap('lswitch'))

    @requireuuid
    def delete(self):
        """
        Delete (verb) will delete the logical switch
        Requires a UUID set at the object.
        """
        uri = "%s/%s" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('DELETE', uri)

    @requireuuid
    def status(self):
        """
        Status (verb) will return the network status of the logical switch
        Requires a UUID set at the object.
        """
        uri = "%s/%s/status" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('GET', uri)

    @requireuuid
    def read(self):
        """
        Read (verb) will return the configuration of the logical switch
        Requires a UUID set at the object.
        """
        uri = "%s/%s" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('GET', uri)

    @requireuuid
    def update(self):
        """
        Update (verb) will update the logical switch
        Requires a UUID set at the object.
        """
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
