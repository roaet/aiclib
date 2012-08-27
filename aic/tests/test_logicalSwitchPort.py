
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

    def test_switchport_create(self):
        pass
