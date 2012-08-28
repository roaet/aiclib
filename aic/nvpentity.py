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
        """Will set/update the tag list of the object.

        Arguments:
        tagList -- a list of dictionaries with the following format:
        {
            'tag':<some value>,  <--- is required
            'scope':<some value>
        }
        If a list is not given and only a dictionary is given it will put the
        dictionary in a list for you.
        """
        if not type(taglist) is list:
            taglist = [taglist]
        elif len(taglist) > 5:
            raise AttributeError("Tag list only supports up to 5 elements")
        self.info['tags'] = taglist
        return self

    def display_name(self, name):
        """Will set/update the display name of the object. By default if a
        display name is not given the generated UUID will be used as the
        display name.

        Arguments:
        name -- a string with max length of 40
        """
        if len(name) > 40:
            raise AttributeError("Display name is greater than 40 characters")
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
        """Will set/update the port_isolation_enabled flag on the switch
        """
        self.info['port_isolation_enabled'] = enabled
        return self

    def transport_zones(self, zones):
        """Will set/update the transport zones that the switch is a 'member' of
        """
        #TODO: Soon
        return self

    def _unroll(self):
        super(LSwitch, self)._unroll()
        return self.info

    def query(self):
        """Returns the query object for logical switches
        """
        queryobject = nvpquery.LSwitchQuery(self.connection,
                                            common.apimap('lswitch'))
        return queryobject

    def create(self):
        """Create (verb) will create the logical switch
        """
        return super(LSwitch, self)._action('POST', common.apimap('lswitch'))

    @requireuuid
    def delete(self):
        """Delete (verb) will delete the logical switch
        Requires a UUID set at the object.
        """
        uri = "%s/%s" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('DELETE', uri)

    @requireuuid
    def status(self):
        """Status (verb) will return the network status of the logical switch
        Requires a UUID set at the object.
        """
        uri = "%s/%s/status" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('GET', uri)

    @requireuuid
    def read(self):
        """Read (verb) will return the configuration of the logical switch
        Requires a UUID set at the object.
        """
        uri = "%s/%s" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('GET', uri)

    @requireuuid
    def update(self):
        """Update (verb) will update the logical switch
        Requires a UUID set at the object.
        """
        uri = "%s/%s" % (common.apimap('lswitch'), self.uuid)
        return super(LSwitch, self)._action('PUT', uri)


class LSwitchPort(NVPEntity):

    def __init__(self, connection, lswitch_uuid, uuid=None):
        super(LSwitchPort, self).__init__(connection)
        self.lswitch_uuid = lswitch_uuid
        self.uuid = uuid

    def admin_status_enabled(self, enabled):
        self.info['admin_status_enabled'] = enabled
        return self

    def allowed_address_pairs(self, address_pair_list):
        """Will set/update the address pair list of the object.

        Arguments:
        addressPairList -- a list of dictionaries with the following format:
        {
            'mac':<some value>,  <--- is required
            'ip':<some value>
        }
        If a list is not given and only a dictionary is given it will put the
        dictionary in a list for you.
        """
        if not type(address_pair_list) is list:
            address_pair_list = [address_pair_list]
        self.info['allowed_address_pairs'] = address_pair_list
        return self

    def mirror_targets(self, mirrorlist):
        """Will set/update the mirror target list of the object.

        Arguments:
        mirror_targets -- a list of IPs that can have up to 3 items
        """
        if not type(mirrorlist) is list:
            mirrorlist = [mirrorlist]
        elif len(mirrorlist) > 3:
            raise AttributeError("Mirror list has greater than 3 items")
        self.info['mirror_targets'] = mirrorlist
        return self

    def portno(self, portnum):
        """Will set/update the port number of the object.

        Arguments:
        portnum -- a integer between 1 and 1000000 inclusive
        """
        if portnum < 1 or portnum > 1000000:
            raise AttributeError("Port number value out of range (1,1000000)")
        self.info['portno'] = portnum
        return self

    def qosuuid(self, uuid):
        """Will set/update the QoS queue UUID of the object.

        Arguments:
        uuid -- a string or None, if None is used 'null' will be sent and the
                QoS UUID of the object will be unset
        """
        if uuid is None:
            uuid = 'null'
        self.info['queue_uuid'] = uuid
        return self

    def security_profiles(self, uuidlist):
        """Will set/update the security profile list of of the object.

        Arguments:
        uuidlist -- A list of strings in UUID format
        If a list is not given and only a single UUID string is given it will
        put the string in a list for you.
        """
        if not type(uuidlist) is list:
            uuidlist = [uuidlist]
        self['security_profiles'] = uuidlist
        return self

    def _unroll(self):
        super(LSwitchPort, self)._unroll()
        return self.info

    def create(self):
        """Create (verb) will create the logical port on the switch"""
        uri = "%s/%s/%s" % (common.apimap('lswitch'), self.lswitch_uuid,
                            'lport')
        return super(LSwitchPort, self)._action("POST", uri)

    @requireuuid
    def read(self):
        """Read (verb) will read the logical port's configuration"""
        uri = "%s/%s/%s/%s" % (common.apimap('lswitch'),
                               self.lswitch_uuid, 'lport', self.uuid)
        return super(LSwitchPort, self)._action("GET", uri)

    @requireuuid
    def status(self):
        """Status (verb) will return the logical port's status"""
        uri = "%s/%s/%s/%s/status" % (common.apimap('lswitch'),
                                      self.lswitch_uuid, 'lport', self.uuid)
        return super(LSwitchPort, self)._action("GET", uri)

    @requireuuid
    def delete(self):
        """Delete (verb) will delete the logical port.
        Requires a UUID set at the object"""
        uri = "%s/%s/%s/%s" % (common.apimap('lswitch'), self.lswitch_uuid,
                               'lport', self.uuid)
        return super(LSwitchPort, self)._action("DELETE", uri)
