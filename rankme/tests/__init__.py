from django.test import TestCase

import mock


# TODO: this should really be moved to a separate tests utils package
class RankMeTestCase(TestCase):
    def setUp(self):
        self.patcher = mock.patch('apps.slack.Slacker')
        self.mock_slacker = self.patcher.start()
        super().setUp()

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()
