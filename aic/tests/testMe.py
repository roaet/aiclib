from aic import test


class TestMe(test.Test):

    def testSomething(self):
        self.assertTrue(True, msg="Should never fail")
