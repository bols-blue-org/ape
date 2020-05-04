import array
from datetime import datetime

from pymavlink import mavutil

from ape.data_collection import AttDataCollection


class LoadBinLog(AttDataCollection):
    def __init__(self, filename):
        self.list = []
        mlog = mavutil.mavlink_connection(filename)
        while True :
            m = mlog.recv_match()
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
            meta = {"type": m.get_type(), "timestamp": datetime.fromtimestamp(timestamp).isoformat()}
            # meta["srcSystem"] = m.get_srcSystem()
            # meta["srcComponent"] = m.get_srcComponent()

            data = m.to_dict()

            del data['mavpackettype']
            if 'data' in data and type(data['data']) is not dict:
                data['data'] = list(data['data'])

            for key in data.keys():
                if type(data[key]) == array.array:
                    data[key] = list(data[key])
            outMsg = {"meta": meta, "data": data}

            self.list.append(outMsg)
        super().__init__(self.list)

