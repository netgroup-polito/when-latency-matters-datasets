import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


def parse_tcpdump_file(path, name, start):
    file = os.path.join(path, name)
    print(f"Opening {file}")
    data = pd.read_csv(file)

    x = data["#frame-timestamp"]*1e3 - start
    y = data["tcp-ack-rtt"]*1e3

    return x, y


def parse_e2e_file(path, name, start):
    file = os.path.join(path, name)
    print(f"Opening {file}")
    data = pd.read_csv(file)

    x = data["#client-send-timestamp"]
    y = data["e2e-rtt"]

    x = x/1e6 - start + y
    return x, y


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    parser.add_argument("output_file", help="Output file")
    args = parser.parse_args()

    results = pd.DataFrame()

    all_bars = {
        "cubic": np.array([1616691476537157339, 1616691486542780584, 1616691516549114496, 1616691526555277290, 1616691556562413352]),
        "bbr": np.array([1616691632955571308, 1616691642961328794, 1616691672968735173, 1616691682973548204, 1616691712980383002]),
    }

    for cc in ["cubic", "bbr"]:
        start = all_bars[cc][0] / 1e6
        e2e_x, e2e_y = parse_e2e_file(args.input_path, f"{cc}-aks-i10.x1024.csv", start)
        tcp_x, tcp_y = parse_tcpdump_file(args.input_path, f"{cc}-aks-tcpdump_report.csv", start)

        results[f"{cc}-tcp-x"] = tcp_x
        results[f"{cc}-tcp-y"] = tcp_y
        results[f"{cc}-e2e-x"] = e2e_x
        results[f"{cc}-e2e-y"] = e2e_y

        plt.plot(tcp_x/1000, tcp_y)
        plt.plot(e2e_x/1000, e2e_y)
        for line in [10, 40, 50, 80]:
            plt.axvline(line)

    results.to_csv(args.output_file, index=False, float_format='%.3f')

    plt.xlabel("Time (s)")
    plt.ylabel("RTT (ms)")
    plt.show()
