from django.test import TestCase

import mock


class RankMeTestCase(TestCase):
    def setUp(self):
        self.patcher = mock.patch('slack.Slacker')
        self.mock_slacker = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
