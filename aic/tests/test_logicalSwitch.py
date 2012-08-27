"""
Created: August 27, 2012

@author: Justin Hammond, Rackspace Hosting
"""

from aic import test
import aic


class TestLogicalSwitch(test.TestCase):

    def setUp(self):
        self.nvp = aic.nvp.Connection("https://nvp")
        self.switch = self.nvp.lswitch().create()

    def tearDown(self):
        if self.switch:
            self.nvp.lswitch(self.switch).delete()

    def test_switch_read(self):
        switch_info = self.nvp.lswitch(self.switch).read()
        self.assertTrue(switch_info['type'] == 'LogicalSwitchConfig',
                        "Switch info should be the correct type")

    def test_switch_status(self):
        switch_status = self.nvp.lswitch(self.switch).status()
        self.assertTrue(switch_status['type'] == 'LogicalSwitchStatus',
                        "Switch status should be the correct type")

    def test_switch_query(self):
        query = self.nvp.lswitch().query()
        query_results = query.uuid(self.switch['uuid']).results()
        self.assertTrue(query_results['result_count'] == 1,
                        "Query on UUID should return single result")

    def test_switch_update(self):
        current_name = self.switch['display_name']
        new_name = "test%s" % current_name
        switch_object = self.nvp.lswitch(self.switch)
        changed_switch = switch_object.display_name(new_name).update()
        self.assertTrue(changed_switch['display_name'] == new_name and
                        self.switch['display_name'] == current_name and
                        changed_switch['uuid'] == self.switch['uuid'],
                        "Data on same UUID should be different post update")
