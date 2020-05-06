#!/usr/bin/env python
# Include standard modules
import argcomplete, argparse

import ape
from ape.load_bin_log import LoadBinLog


def evaluation(log_file):
    data = LoadBinLog(log_file, ["CTUN", "ATT"])
    index = 0
    print_flg = False
    data = data.dropWithAlt(1)
    result = 0
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
            result += abs(tmp["DesRoll"] - tmp["Roll"])
            if first is None:
                first = item

        # print("インデックス：" + str(index) + ", 値：" + str(item))
        index += 1

    dt1 = first["meta"]["timestamp"]
    dt2 = last["meta"]["timestamp"]

    print("start=" + str(dt1) + " end=" + str(dt2))
    td = dt2 - dt1
    ave = result / td.seconds
    print("result average=" + str(ave) + " flight time:" + str(td) + "result total:" + str(result))


def main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=str, help="log file")
    parser.add_argument("-V", "--version", action='version',
                        version=ape.__version__, help="show program version")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    # Read arguments from the command line
    args = parser.parse_args()

    if args.log is None:
        print("must logfile name")
        exit(-1)
    evaluation(args.log)


if __name__ == "__main__":
    main()
