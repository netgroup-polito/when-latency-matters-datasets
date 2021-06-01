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


def summary(data):
    mn = np.min(data)
    lw = np.percentile(data, 1)
    lq = np.percentile(data, 25)
    me = np.percentile(data, 50)
    uq = np.percentile(data, 75)
    uw = np.percentile(data, 99)
    mx = np.max(data)

    print(f"{mn:5.2f}  {lw:5.2f}  {lq:5.2f}  {me:5.2f}  {uq:5.2f}  {uw:5.2f}  {mx:5.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    args = parser.parse_args()

    print(" Min    P1     P25    P50    P75    P99.0  Max")
    for ep in [
        "on-prem-to-on-prem", "on-prem-1-to-aws-milan", "on-prem-1-to-aks-ch",
        "on-prem-2-to-aks-ch", "on-prem-1-to-aks-fr", "on-prem-1-to-aws-fr",
        "on-prem-1-to-aws-uk", "on-prem-2-to-aws-uk", "aks-uk-to-aws-uk"]:

        data = parse_e2e_file(args.input_path, f"*-*{ep}*.i*.x10240.csv")
        summary(data)
