import array
from datetime import datetime, timezone, timedelta

from pymavlink import mavutil

from ape.data_collection import DataCollection


class LoadBinLog(DataCollection):
    def __init__(self, filename, data_type=None):
        self.list = []
        mlog = mavutil.mavlink_connection(filename)
        while True:
            m = mlog.recv_match(type=data_type)
            timestamp = getattr(m, '_timestamp', 0.0)
            if m is None:
                break
            if m.get_type() == "FMT":
                continue
            if m.get_type() == "PARAM_VALUE":
                continue
            if m.get_type() == "PARM":
                continue
            if m.get_type() == "FMTU":
                continue
            if m.get_type() == "UNIT":
                continue
            jst = timezone(timedelta(hours=+9), 'JST')
            meta = {"type": m.get_type(), "timestamp": datetime.fromtimestamp(timestamp, tz=jst)}
            # meta["srcSystem"] = m.get_srcSystem()
            # meta["srcComponent"] = m.get_srcComponent()

            data = m.to_dict()

            del data['mavpackettype']
            if 'data' in data and type(data['data']) is not dict:
                data['data'] = list(data['data'])

            for key in data.keys():
                if type(data[key]) == array.array:
                    data[key] = list(data[key])
            out_msg = {"meta": meta, "data": data}

            self.list.append(out_msg)
        super().__init__(self.list)

