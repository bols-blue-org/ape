import json
from copy import copy
from datetime import datetime
from typing import Union, List, Dict


class DataCollection:
    data =[]
    init_alt = 0

    def __init__(self, file: Union[List, str], init_alt=None):
        self._i = 0
        if type(file) is list:
            self.data = file
        else:
            json_load = json.load(file)
            self.data = json_load
        if init_alt == None :
            for item in self.data:
                if item["meta"]["type"] == "CTUN":
                    self.init_alt = item["data"]["Alt"]
                    break
        else:
            self.init_alt = init_alt

    def selectWithType(self, type_name):
        new_data = []
        for item in self.data:
            if item["meta"]["type"] == type_name:
                new_data.append(item)
        return DataCollection(new_data, init_alt=self.init_alt)

    def dropWithType(self, type_name):
        new_data = []
        for item in self.data:
            if item["meta"]["type"] != type_name:
                new_data.append(item)
        return DataCollection(new_data, init_alt=self.init_alt)

    def dropWithAlt(self, alt_diff):
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

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self) -> Dict[str, Dict[str,Union[str,float,datetime]]]:
        if self._i == len(self.data):
            raise StopIteration()
        value = self.data[self._i]
        self._i += 1
        return value

    def __reversed__(self):
        tmp = copy(self.data)
        tmp.reverse()
        return DataCollection(tmp, init_alt=self.init_alt)
