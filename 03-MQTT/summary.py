import argparse
import glob
import numpy as np
import os
import pandas as pd


def parse_e2e_file(path, name):
    full_path = os.path.join(path, name)
    e2e_rtt = np.array([], dtype=float)
    for file in glob.glob(full_path):
        data = pd.read_csv(file)
        e2e_rtt = np.append(e2e_rtt, data["e2e-rtt"])
    return e2e_rtt


def boxplot(data):
    mn = np.min(data)
    lw = np.percentile(data, 1)
    lq = np.percentile(data, 25)
    me = np.percentile(data, 50)
    uq = np.percentile(data, 75)
    ur = np.percentile(data, 90)
    uw = np.percentile(data, 99)
    mx = np.max(data)

    print(f"{mn:5.2f}  {lw:5.2f}  {lq:5.2f}  {me:5.2f}  {uq:5.2f}  {ur:5.2f}  {uw:5.2f}  {mx:5.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    args = parser.parse_args()

    print(" Min    P1     P25    P50    P75    P90    P99.0  Max")
    for size in [1024, 10240, 102400]:
        for type in ["plain", "mqtt-qos0", "mqtt-qos1", "mqtt-qos2"]:
            data = parse_e2e_file(args.input_path, f"{type}*{size}.csv")
            boxplot(data)

        print()
