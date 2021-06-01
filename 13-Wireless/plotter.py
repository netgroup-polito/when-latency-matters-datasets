import argparse
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import yaml


def parse_e2e_file(full_path):
    e2e_rtt = np.array([], dtype=float)
    print(f"Opening {file}")
    data = pd.read_csv(file)
    e2e_rtt = np.append(e2e_rtt, data["e2e-rtt"])
    return e2e_rtt


def plot_cdf(data, label):
    x = np.sort(data)
    y = np.linspace(0, 1, len(data), endpoint=False)
    plt.plot(x, y, label=label)


def get_endpoint(path):
    full_path = os.path.join(path, "settings-crownlabs*.yaml")
    with open(glob.glob(full_path)[0]) as file:
        settings = yaml.safe_load(file)
        return settings.get("endpoints")[0].get("description")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    parser.add_argument("pattern", help="Pattern")
    parser.add_argument("--xmax", help="The xmax value", default=15, type=float)
    parser.add_argument("--title", help="The title of the graph")
    args = parser.parse_args()

    path = os.path.join(args.input_path, f"{args.pattern}*")
    endpoints = []
    for file in sorted(glob.glob(path)):
        e2e_data = parse_e2e_file(file)
        plot_cdf(e2e_data, label=file)

    plt.xlim(left=0, right=args.xmax)
    plt.ylim(bottom=0, top=1)
    plt.xlabel("RTT (ms)")
    plt.ylabel("CDF")
    plt.title(args.title)
    plt.legend()
    plt.show()
