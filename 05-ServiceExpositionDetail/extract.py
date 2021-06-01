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


def x_values(samples):
    return np.concatenate((
        np.linspace(0, 90, samples, endpoint=False),
        np.linspace(90, 99, samples, endpoint=False),
        np.linspace(99, 99.9, samples, endpoint=False),
        np.linspace(99.9, 99.99, samples, endpoint=False),
        np.linspace(99.99, 99.991, int(samples/10), endpoint=False),
    ))


def cdf(data, idxes):
    cdf = np.sort(data)
    return cdf[[int(len(data) * i) for i in idxes]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input folder")
    parser.add_argument("output_file", help="Output file")
    args = parser.parse_args()

    size = 10240

    samples = 250
    x = x_values(samples)
    results = pd.DataFrame(100 - x, columns=['x'])

    lbs = ["bare", "same-notls", "same-tls", "diff", "ingress"]
    eps = ["bare-server", "load-balancer-local", "load-balancer-local-tls", "load-balancer-cluster-tls", "reverse-proxy-tls"]

    for lb, ep in zip(lbs, eps):
        data = parse_e2e_file(args.input_path, f"*-{ep}.i*.x{size}.csv")
        results[lb] = cdf(data, x / 100)

    results.to_csv(args.output_file, index=False, float_format='%.4f')
