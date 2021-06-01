import argparse
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def cdf(data):
    x = np.sort(data)
    y = np.linspace(0, 1, len(x))
    return (x, y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", help="Input files", nargs='+')
    parser.add_argument("--xmax", help="X Max", type=int, default=50)

    args = parser.parse_args()

    for i, file in enumerate(sorted(args.input_files)):
        print(f"Processing file: {file}")
        data = pd.read_csv(file)
        plt.boxplot(data['e2e-rtt'], whis=[1, 99], positions=[i, ], vert=False, sym="", widths=0.5, labels=[file.split('/')[-1], ])

    plt.xlim(0, args.xmax)
    plt.xlabel("FCT (ms)")
    plt.show()
