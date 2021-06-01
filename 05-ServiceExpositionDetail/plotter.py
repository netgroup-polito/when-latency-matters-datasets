import argparse
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


def parse_e2e_file(path, name, skip):
    full_path = os.path.join(path, name)
    e2e_rtt = np.array([], dtype=float)
    for file in sorted(glob.glob(full_path)):
        print(f"Opening {file}")
        data = pd.read_csv(file)
        e2e_rtt = np.append(e2e_rtt, data["e2e-rtt"][skip:])
    return e2e_rtt


def plot_cdf(data, label):
    y = np.sort(data)
    x = np.linspace(0, 100, len(data), endpoint=False)
    plt.semilogx([100.0 - v for v in x], y, label=label)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    parser.add_argument("run", help="The run to plot", nargs='?', default='*')
    parser.add_argument("--skip", help="The number of initial samples to skip", type=int, default=0)
    args = parser.parse_args()

    size = 10240
    for ep in ["bare-server", "load-balancer-local", "load-balancer-local-tls", "load-balancer-cluster-tls", "reverse-proxy-tls"]:
        data = parse_e2e_file(args.input_path, f"{args.run}-{ep}.i*.x{size}.csv", args.skip)
        plot_cdf(data, ep)

    plt.gca().invert_xaxis()
    plt.ylabel("FCT (ms)")
    plt.xlim(left=100, right=.01)
    plt.ylim(bottom=0, top=25)
    plt.xticks(ticks=[1e-2, 1e-1, 1e0, 1e1, 1e2], labels=["99.99%", "99.9%", "99%", "90%", "0%"])
    plt.legend()
    plt.title(f"Run: {args.run}")
    plt.show()
