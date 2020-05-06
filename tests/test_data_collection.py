import unittest

from ape.data_collection import DataCollection


class DataCollectionTestCase(unittest.TestCase):
    def test_loadjson(self):
        json_open = open('../tests/log_0_2020-5-1-14-53-42.bin.json', 'r')
        data = DataCollection(json_open)
        self.assertGreater(len(data), 0, "no data")

    def test_dropWithType(self):
        json_open = open('../tests/log_0_2020-5-1-14-53-42.bin.json', 'r')
        data = DataCollection(json_open)
        test_type = "RCOU"
        flg = False
        for item in data:
            if item["meta"]["type"] == test_type:
                flg = True
        self.assertTrue(flg,"need json data "+test_type)
        data = data.dropWithType(test_type)
        flg = False
        for item in data:
            if item["meta"]["type"] == test_type:
                flg = True
        self.assertGreater(len(data), 0, "no data")
        self.assertFalse(flg, "not drop "+test_type)

    def test_selectWithAlt(self):
        json_open = open('../tests/log_0_2020-5-1-14-53-42.bin.json', 'r')
        data = DataCollection(json_open)
        test_type = "RCOU"
        flg = False
        for item in data:
            if item["meta"]["type"] != test_type:
                flg = True
        self.assertTrue(flg,"need json data "+test_type)
        data = data.selectWithType(test_type)
        flg = False
        for item in data:
            # print("値：" + str(item))
            if item["meta"]["type"] != test_type:
                flg = True
        self.assertGreater(len(data), 0, "no select data")
        self.assertFalse(flg, "not  "+test_type)


    def test_dropWithAlt(self):
        json_open = open('../tests/log_0_2020-5-1-14-53-42.bin.json', 'r')
        data = DataCollection(json_open)
        data = data.dropWithAlt(2)
        flg = False
        data = data.selectWithType("CTUN")
        for item in data:
            if item["data"]["Alt"] < data.init_alt + 2:
                flg = True
        self.assertGreater(len(data), 0, "no data")
        self.assertFalse(flg, "not drop Alt")

if __name__ == '__main__':
    unittest.main()
