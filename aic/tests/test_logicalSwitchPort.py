
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
        self.switchport = self.nvp.lswitch_port(self.switch).create()

    def tearDown(self):
        if self.switchport:
            self.nvp.lswitch_port(self.switchport).delete()
        if self.switch:
            self.nvp.lswitch(self.switch).delete()

    def test_switchport_create(self):
        self.assertTrue(True)
