"""
Created: August 30, 2012

@author: Justin Hammond, Rackspace Hosting
"""

from aic import test
import aic


class TestQOS(test.TestCase):

    def setUp(self):
        self.nvp = aic.nvp.Connection("https://nvp")
        self.qos = self.nvp.qos().create()

    def tearDown(self):
        if self.qos:
            self.nvp.qos(self.qos).delete()

    def test_qos_create(self):
        """Functionality is implicit in setUp and tearDown. If this passes
        those must have passed"""
        self.assertTrue(True)

    def test_qos_read(self):
        qos_info = self.nvp.qos(self.qos).read()
        self.assertTrue(qos_info['uuid'] == self.qos['uuid'],
                        "qos uuid should be the same UUID as stored")

    def test_qos_delete(self):
        """Functionality is implicit in setUp and tearDown. If this passes
        those must have passed"""
        self.assertTrue(True)

    def test_qos_query(self):
        query = self.nvp.qos().query()
        query_results = query.uuid(self.qos['uuid']).results()
        self.assertTrue(query_results['result_count'] == 1,
                        "Query on UUID should return single result")

    def test_qos_update(self):
        current_name = self.qos['display_name']
        new_name = "test%s" % current_name
        qos_object = self.nvp.qos(self.qos)
        changed_qos = qos_object.display_name(new_name).update()
        self.assertTrue(changed_qos['display_name'] == new_name and
                        self.qos['display_name'] == current_name and
                        changed_qos['uuid'] == self.qos['uuid'],
                        "Data on same UUID should be different post update")
