import unittest


class TestAPI(unittest.TestCase):
    def test_01_search_in_file(self):
        try:
            from mgrep import search_in_file
        except ImportError:
            self.fail("Could not import 'search_in_file' from 'mgrep' module.")

    def test_02_run_multi_threaded(self):
        try:
            from mgrep import run_multi_threaded
        except ImportError:
            self.fail("Could not import 'run_multi_threaded' from 'mgrep' module.")
