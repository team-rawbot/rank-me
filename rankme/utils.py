from django.test import TestCase

import mock


# TODO: this should really be moved to a separate tests utils package
class RankMeTestCase(TestCase):
    def setUp(self):
        self.patcher = mock.patch('slack.Slacker')
        self.mock_slacker = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()


def memoize(function):
    """
    Copied from http://stackoverflow.com/questions/815110/is-there-a-decorator-to-simply-cache-function-return-values
    """
    memo = {}

    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
        memo[args] = rv
        return rv
    return wrapper
