import argparse
import glob
import numpy as np
import os
import pandas as pd
import re


def parse_ping_file(path, name):
    file = os.path.join(path, name)
    ping_rtt = np.array([], dtype=float)
    print(f"Opening {file}")
    with open(file) as lines:
        for line in lines:
            match = re.match(r'.*time=([0-9]+(\.[0-9]+)?).*', line)
            if match:
                ping_rtt = np.append(ping_rtt, float(match.group(1)))
    return ping_rtt


def parse_tcpdump_files(path, name):
    full_path = os.path.join(path, name)
    tcp_rtt = np.array([], dtype=float)
    for file in glob.glob(full_path):
        print(f"Opening {file}")
        data = pd.read_csv(file)
        tcp_rtt = np.append(tcp_rtt, data["tcp-ack-rtt"]*1e3)
    return tcp_rtt


def parse_e2e_file(path, name):
    full_path = os.path.join(path, name)
    e2e_rtt = np.array([], dtype=float)
    for file in glob.glob(full_path):
        print(f"Opening {file}")
        data = pd.read_csv(file)
        e2e_rtt = np.append(e2e_rtt, data["e2e-rtt"])
    return e2e_rtt


def cdf(data, samples):
    cdf = np.sort(data)
    return cdf[np.linspace(0, len(cdf)-1, samples, dtype=int)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    parser.add_argument("output_file", help="Output file")
    args = parser.parse_args()

    ping_node = parse_ping_file(args.input_path, "ping_node.txt")
    ping_router = parse_ping_file(args.input_path, "ping_router.txt")

    tcp_data_1k = parse_tcpdump_files(args.input_path, "*-tcpdump_report_x1024.csv")
    e2e_data_1k = parse_e2e_file(args.input_path, "*-flow-completion-time.i10.x1024.csv")

    tcp_data_100k = parse_tcpdump_files(args.input_path, "*-tcpdump_report_x102400.csv")
    e2e_data_100k = parse_e2e_file(args.input_path, "*-flow-completion-time.i10.x102400.csv")

    samples = 1000
    results = pd.DataFrame(np.linspace(0, 1, samples, endpoint=False), columns=['y'])

    results["ping-node"] = cdf(ping_node, samples)
    results["ping-router"] = cdf(ping_router, samples)
    results["tcp-rtt-1"] = cdf(tcp_data_1k, samples)
    results["tcp-rtt-100"] = cdf(tcp_data_100k, samples)
    results["app-fct-1"] = cdf(e2e_data_1k, samples)
    results["app-fct-100"] = cdf(e2e_data_100k, samples)

    results.to_csv(args.output_file, index=False, float_format='%.3f')

    print(results.describe(percentiles=[0.01, 0.10, 0.25, 0.5, 0.75, 0.9, 0.99]))
