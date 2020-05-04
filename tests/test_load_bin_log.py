import unittest

from ape.load_bin_log import LoadBinLog


class LoadBinTestCase(unittest.TestCase):
    def test_something(self):
        data = LoadBinLog("../tests/log_0_2020-5-1-14-53-42.bin")
        self.assertGreater(len(data), 0, "no data")

if __name__ == '__main__':
    unittest.main()
