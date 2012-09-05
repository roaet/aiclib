"""
Created: August 30, 2012

@author: Justin Hammond, Rackspace Hosting
"""

from aiclib import test
import aiclib


class TestTransportNode(test.TestCase):

    def setUp(self):
        self.nvp = aiclib.nvp.Connection("https://nvp")
        self.tnode = self.nvp.transportnode().create()

    def tearDown(self):
        if self.tnode:
            self.nvp.transportnode(self.tnode).delete()

    def test_tnode_create(self):
        """Functionality is implicit in setUp and tearDown. If this passes
        those must have passed"""
        self.assertTrue(True)

    def test_tnode_read(self):
        qos_info = self.nvp.transportnode(self.tnode).read()
        self.assertTrue(qos_info['uuid'] == self.tnode['uuid'],
                        "qos uuid should be the same UUID as stored")

    def test_tnode_delete(self):
        """Functionality is implicit in setUp and tearDown. If this passes
        those must have passed"""
        self.assertTrue(True)

    def test_tnode_query(self):
        query = self.nvp.transportnode().query()
        query_results = query.uuid(self.tnode['uuid']).results()
        self.assertTrue(query_results['result_count'] == 1,
                        "Query on UUID should return single result")

    def test_tnode_update(self):
        current_name = self.tnode['display_name']
        new_name = "test%s" % current_name
        tnode_object = self.nvp.transportnode(self.tnode)
        changed_tnode = tnode_object.display_name(new_name).update()
        self.assertTrue(changed_tnode['display_name'] == new_name and
                        self.tnode['display_name'] == current_name and
                        changed_tnode['uuid'] == self.tnode['uuid'],
                        "Data on same UUID should be different post update")
