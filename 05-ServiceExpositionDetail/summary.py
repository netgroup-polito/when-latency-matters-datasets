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
    ux = np.percentile(data, 99.5)
    uy = np.percentile(data, 99.9)
    uz = np.percentile(data, 99.95)
    ua = np.percentile(data, 99.99)
    mx = np.max(data)

    print(f"{mn:5.2f}  {lw:5.2f}  {lq:5.2f}  {me:5.2f}  {uq:5.2f}  {ur:5.2f}  {uw:5.2f}  {ux:5.2f}  {uy:5.2f}  {uz:5.2f}  {ua:5.2f}  {mx:5.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    parser.add_argument("run", help="The run to summarize", nargs='?', default='*')
    args = parser.parse_args()

    print(" Min    P1     P25    P50    P75    P90    P99.0  P99.5  P99.9 P99.95 P99.99 Max")
    for ep in ["bare-server", "load-balancer-local", "load-balancer-local-tls", "load-balancer-cluster-tls", "reverse-proxy-tls"]:
        data = parse_e2e_file(args.input_path, f"{args.run}-{ep}.i*.x10240.csv")
        boxplot(data)

    print()
