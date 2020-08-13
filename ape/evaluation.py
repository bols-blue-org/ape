#!/usr/bin/env python
# Include standard modules
from datetime import datetime

import argcomplete
import argparse

import ape
from ape.load_bin_log import LoadBinLog

def angle_evaluation(data):
    index = 0
    roll_result = 0
    pitch_result = 0
    yaw_result = 0
    rev = reversed(data)
    first = None
    last = None
    for item in rev:
        if item["meta"]["type"] == "ATT":
            last = item
            break

    for item in data:
        if item["meta"]["type"] == "ATT":
            tmp = item["data"]
            roll_result += abs(tmp["DesRoll"] - tmp["Roll"])
            pitch_result += abs(tmp["DesPitch"] - tmp["Pitch"])
            yaw_result += abs(tmp["DesYaw"] - tmp["Yaw"])
            if first is None:
                first = item

        # print("インデックス：" + str(index) + ", 値：" + str(item))
        index += 1

    dt1 :datetime= first["meta"]["timestamp"]
    dt2 = last["meta"]["timestamp"]

    print("start=" + str(dt1) + " end=" + str(dt2))
    td = dt2 - dt1
    print("flight time:" + str(td))
    ave = roll_result / td.seconds
    print("roll result average=" + str(ave) + " roll result total:" + str(roll_result))
    ave = pitch_result / td.seconds
    print("pitch result average=" + str(ave) + " roll result total:" + str(pitch_result))
    ave = yaw_result / td.seconds
    print("yaw result average=" + str(ave) + " roll result total:" + str(yaw_result))

def angular_evaluation(data):
    index = 0
    roll_result = 0
    pitch_result = 0
    yaw_result = 0
    rev = reversed(data)
    first = None
    last = None
    for item in rev:
        if item["meta"]["type"] == "RATE":
            last = item
            break

    for item in data:
        if item["meta"]["type"] == "RATE":
            tmp = item["data"]
            roll_result += abs(tmp["RDes"] - tmp["R"])
            pitch_result += abs(tmp["PDes"] - tmp["P"])
            yaw_result += abs(tmp["YDes"] - tmp["Y"])
            if first is None:
                first = item

        # print("インデックス：" + str(index) + ", 値：" + str(item))
        index += 1

    dt1 :datetime= first["meta"]["timestamp"]
    dt2 = last["meta"]["timestamp"]

    print("start=" + str(dt1) + " end=" + str(dt2))
    td = dt2 - dt1
    print("flight time:" + str(td))
    ave = roll_result / td.seconds
    print("roll result average=" + str(ave) + " roll result total:" + str(roll_result))
    ave = pitch_result / td.seconds
    print("pitch result average=" + str(ave) + " roll result total:" + str(pitch_result))
    ave = yaw_result / td.seconds
    print("yaw result average=" + str(ave) + " roll result total:" + str(yaw_result))

def evaluation(log_file):
    data = LoadBinLog(log_file, ["CTUN", "ATT", "RATE"])
    data = data.dropWithAlt(1)
    print("============= angle evaluation ================")
    angle_evaluation(data)
    print("============= angular evaluation ================")
    angular_evaluation(data)


def main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=str, help="log file")
    parser.add_argument("-V", "--version", action='version',
                        version=ape.__version__, help="show program version")
    argcomplete.autocomplete(parser)
    # Read arguments from the command line
    args = parser.parse_args()

    if args.log is None:
        print("must logfile name")
        exit(-1)
    evaluation(args.log)


if __name__ == "__main__":
    main()
