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


def boxplot(data, pos, cm, outliers_lower=5, outliers_upper=10):
    lw = np.percentile(data, 1)
    lq = np.percentile(data, 25)
    me = np.percentile(data, 50)
    uq = np.percentile(data, 75)
    uw = np.percentile(data, 99)

    lower = np.sort(data[data < lw - 0.05])
    lower_idx = np.linspace(0, len(lower), num=len(lower) if len(lower) < outliers_lower else outliers_lower, endpoint=False, dtype=int)
    lower = np.array2string(lower[lower_idx], precision=2, separator="\\\\", max_line_width=1000)

    upper = np.sort(data[data > uw + 0.05])
    upper_idx = np.linspace(0, len(upper), num=len(upper) if len(upper) < outliers_upper else outliers_upper, endpoint=False, dtype=int)
    upper = np.array2string(upper[upper_idx], precision=2, separator="\\\\", max_line_width=1000)

    return (
        f"\\addplot+ [black, boxplot prepared={{lower whisker={lw:.2f}, lower quartile={lq:.2f}, median={me:.2f}, upper quartile={uq:.2f}, upper whisker={uw:.2f}, }}, "
        f"boxplot/draw position={pos}, index of colormap={cm}, mark=+, every mark/.append style={{mark size=1pt, line width=0.2pt}}] table\n"
        f"    [row sep=\\\\, y index=0] {{ data\\\\ {lower[1:-1]} \\\\ {upper[1:-1]}\\\\}};"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    args = parser.parse_args()

    position = 1

    for interval in [25, 100, 200, 300, 500, 1000, 2000]:

        data = parse_e2e_file(args.input_path, f"?-*.i{interval}.x102400.csv")
        text = boxplot(data, position, 0, outliers_lower=10, outliers_upper=30)
        print(text)

        position = position + 1
