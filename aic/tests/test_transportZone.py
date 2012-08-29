"""
Created: August 29, 2012

@author: Justin Hammond, Rackspace Hosting
"""

from aic import test
import aic


class TestTransportZone(test.TestCase):

    def setUp(self):
        self.nvp = aic.nvp.Connection("https://nvp")
        self.zone = self.nvp.zone().create()

    def tearDown(self):
        if self.zone:
            self.nvp.zone(self.zone).delete()

    def test_transportzone_create(self):
        """Functionality is implicit in setUp and tearDown. If this passes
        those must have passed"""
        self.assertTrue(True)

    def test_transportzone_read(self):
        zone_info = self.nvp.zone(self.zone).read()
        self.assertTrue(zone_info['uuid'] == self.zone['uuid'],
                        "Zone uuid should be the same UUID as stored")

    def test_transportzone_delete(self):
        """Functionality is implicit in setUp and tearDown. If this passes
        those must have passed"""
        self.assertTrue(True)

    def test_transportzone_query(self):
        query = self.nvp.zone().query()
        query_results = query.uuid(self.zone['uuid']).results()
        self.assertTrue(query_results['result_count'] == 1,
                        "Query on UUID should return single result")

    def test_transportzone_update(self):
        current_name = self.zone['display_name']
        new_name = "test%s" % current_name
        zone_object = self.nvp.zone(self.zone)
        changed_zone = zone_object.display_name(new_name).update()
        self.assertTrue(changed_zone['display_name'] == new_name and
                        self.zone['display_name'] == current_name and
                        changed_zone['uuid'] == self.zone['uuid'],
                        "Data on same UUID should be different post update")
