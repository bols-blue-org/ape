import unittest

from ape.load_bin_log import LoadBinLog


class LoadBinTestCase(unittest.TestCase):
    def test_LoadBinLogAll(self):
        data = LoadBinLog("../tests/log_0_2020-5-1-14-53-42.bin")
        self.assertGreater(len(data), 0, "no data")

    def test_LoadBinLogString(self):
        data = LoadBinLog("../tests/log_0_2020-5-1-14-53-42.bin", "RCOU")
        self.assertEqual(len(data), 822, "no data")

    def test_LoadBinLogStringArray(self):
        data = LoadBinLog("../tests/log_0_2020-5-1-14-53-42.bin", ["RCOU", "ATT"])
        self.assertEqual(len(data), 1644, "no data")


if __name__ == '__main__':
    unittest.main()
