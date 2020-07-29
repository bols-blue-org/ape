import json
from copy import copy
from datetime import datetime
from typing import Union, List, Dict, IO, Any


class DataCollection:
    """

    """
    data: List[Dict[str, Dict[str, Union[str, float, int, datetime]]]] = []
    init_alt = 0

    def __init__(self, file: Union[List, IO], init_alt=None):
        self._i = 0
        if type(file) is list:
            self.data = file
        else:
            json_load = json.load(file)
            self.data = json_load
        if init_alt is None:
            for item in self.data:
                if item["meta"]["type"] == "CTUN":
                    self.init_alt = item["data"]["Alt"]
                    break
        else:
            self.init_alt = init_alt

    def selectWithType(self, type_name):
        """

        :param type_name:
        :return:
        """
        new_data = []
        for item in self.data:
            if item["meta"]["type"] == type_name:
                new_data.append(item)
        return DataCollection(new_data, init_alt=self.init_alt)

    def dropWithType(self, type_name: str):
        """

        :param type_name:
        :return:
        """
        new_data = []
        for item in self.data:
            if item["meta"]["type"] != type_name:
                new_data.append(item)
        return DataCollection(new_data, init_alt=self.init_alt)

    def dropWithAlt(self, alt_diff: int):
        """

        :param alt_diff:
        :return: DataCollection
        """
        drop_flg = False
        new_data = []
        for item in self.data:
            if item["meta"]["type"] == "CTUN":
                if item["data"]["Alt"] > self.init_alt + alt_diff:
                    drop_flg = True
                else:
                    drop_flg = False
            if drop_flg:
                new_data.append(item)
        return DataCollection(new_data, init_alt=self.init_alt)

    def seplateRCIN6Param(self):
        """

        :return:
        """
        ret_dict = {}
        new_data = []
        last = 0
        for item in self.data:
            new_data.append(item)
            param_type = item["meta"]["type"]
            if param_type == "RCIN":
                ch6_val = item["data"]["C6"]
                if ch6_val != last:
                    if ch6_val != 0:
                        ret_dict[last] = DataCollection(new_data, init_alt=self.init_alt)
                    last = ch6_val
                    new_data = []
        ret_dict[last] = DataCollection(new_data, init_alt=self.init_alt)
        return ret_dict


    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self) -> Dict[str, Dict[str, Union[str, float, int, datetime]]]:
        if self._i == len(self.data):
            raise StopIteration()
        value = self.data[self._i]
        self._i += 1
        return value

    def __reversed__(self):
        tmp = copy(self.data)
        tmp.reverse()
        return DataCollection(tmp, init_alt=self.init_alt)
