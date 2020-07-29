#!/usr/bin/env python
# Include standard modules
import argcomplete
import argparse
import numpy as np
import matplotlib.pyplot as plt

import ape
from ape.load_bin_log import LoadBinLog

XNUM = 0
YNUM = 1
ZNUM = 2

def fft(log_file):
    data = LoadBinLog(log_file, ["CTUN", "IMU"])
    index = 0
    data = data.dropWithAlt(1)
    fft_arry = [[], [], [], []]

    for item in data:
        if item["meta"]["type"] == "IMU":
            tmp = item["data"]
            fft_arry[XNUM].append(tmp["AccX"])
            fft_arry[YNUM].append(tmp["AccY"])
            fft_arry[ZNUM].append(tmp["AccZ"])
            fft_arry[3].append(item["meta"]["timestamp"])


        # print("インデックス：" + str(index) + ", 値：" + str(item))
        index += 1

    # 例の信号を作成
    td =  fft_arry[3][-1] - fft_arry[3][0]
    t = np.linspace(0, td.seconds, len(fft_arry[XNUM]));
    z = 0.1 + 0.2 * np.sin(t * 10 * 2 * np.pi) + 0.2 * np.sin(t * 33 * 2 * np.pi);

    # サンプリング周波数
    fsmp = len(fft_arry[XNUM]) / td.seconds
    freq = np.fft.fft(fft_arry[XNUM])
    freq2 = np.fft.fftfreq(len(fft_arry[XNUM]), d=(1.0 / fsmp) );

    plt.figure(1)
    fig, ax = plt.subplots(nrows=3, sharex=True, figsize=(6, 6))
    ax[0].plot(freq.real, label="FFT")
    ax[0].legend()
    ax[1].plot(freq, freq2);
    ax[1].legend()

    plt.show();

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
    fft(args.log)


if __name__ == "__main__":
    main()
