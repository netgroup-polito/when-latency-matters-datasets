import argparse
import glob
import numpy as np
import os
import pandas as pd


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

    stateless_notls_1k = parse_e2e_file(args.input_path, "stateless.i100.x1024.notls.csv")
    stateless_notls_100k = parse_e2e_file(args.input_path, "stateless.i100.x102400.notls.csv")
    stateless_tls_1k = parse_e2e_file(args.input_path, "stateless.i100.x1024.tls.csv")
    stateless_tls_100k = parse_e2e_file(args.input_path, "stateless.i100.x102400.tls.csv")

    persistent_tls_1k = parse_e2e_file(args.input_path, "persistent.i100.x1024.tls.csv")
    persistent_tls_100k = parse_e2e_file(args.input_path, "persistent.i100.x102400.tls.csv")

    samples = 100
    results = pd.DataFrame(np.linspace(0, 1, samples, endpoint=False), columns=['y'])

    results["stateless-notls-1"] = cdf(stateless_notls_1k, samples)
    results["stateless-notls-100"] = cdf(stateless_notls_100k, samples)
    results["stateless-tls-1"] = cdf(stateless_tls_1k, samples)
    results["stateless-tls-100"] = cdf(stateless_tls_100k, samples)
    results["persistent-tls-1"] = cdf(persistent_tls_1k, samples)
    results["persistent-tls-100"] = cdf(persistent_tls_100k, samples)

    results.to_csv(args.output_file, index=False, float_format='%.3f')

    print(results.describe(percentiles=[0.01, 0.10, 0.25, 0.5, 0.75, 0.9, 0.99]))
