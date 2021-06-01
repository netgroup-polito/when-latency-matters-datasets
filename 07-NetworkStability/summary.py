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


def percentiles(data):
    return np.array([
        np.percentile(data, 50),
        np.percentile(data, 75),
        np.percentile(data, 90),
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    args = parser.parse_args()

    results = list()
    for run in (1 + np.arange(24)):
        data = parse_e2e_file(args.input_path, f"{run}-*")
        results.append(percentiles(data))

    results = np.matrix(results)
    diff = results.max(axis=0) - results.min(axis=0)
    perc = 100 * diff / results.mean(axis=0)
    print("                   P50   P75   P90")
    print(f"Variability (ms): {diff[0,0]:.2f}  {diff[0,1]:.2f}  {diff[0,2]:.2f}")
    print(f"Variability (%):  {perc[0,0]:.2f}  {perc[0,1]:.2f}  {perc[0,2]:.2f}")
