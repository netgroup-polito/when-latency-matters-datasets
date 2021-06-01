# When Latency Matters: Measurements and Lessons Learned - Datasets

This repository contains the full datasets (anonymized replacing the actual IP addresses) and the post-processing scripts used
to plot the graphs presented in the manuscript "When Latency Matters: Measurements and Lessons Learned" submitted to ACM SIGCOMM
Computer Communications Review. The post-processing scripts compute the main statistics about each dataset and return either
the CDF distribution or the instructions to plot the boxplots using the *pgfplots* LaTeX library, depending on the graph type.

Specifically:

* `01-LatencyMetrics` refers to a comparison of the latency distribution at network, TCP and application level.
* `02-StatelessPersistent` refers to a comparison between stateless connections (w/ and w/o TLS) and persistent connections (w/ TLS).
* `03-MQTT` refers to a comparison between WebSocket communication and MQTT, considering different QoS levels.
* `04-ServiceExposition` refers to a comparison between different approaches to expose services in Kubernetes.
* `05-ServiceExpositionDetail` refers to a close-up investigation at high percentiles between different approaches to expose services in Kubernetes.
* `06-ApplicationBehavior` refers to an evaluation showing the effects of the `slow_start_after_idle` TCP behavior on intermittent applications.
* `07-NetworkStability` refers to a 24 hours evaluation showing the stability of the measured flow completion time.
* `08-ECMPRouting` refers to multiple measurements between the same pair of endpoints, showing the effects of ECMP routing.
* `09-EndpointMatrix` refers to measurements between different pairs of endpoints, including on-premise hosts and public data-centers.
* `10-ResidentialCloud` refers to measurements between a client connected to a residential network and multiple public data-centers.
* `11-ResidentialCloudDetail` refers to measurements between multiple client connected to different residential network and public data-centers.
* `12-Buffering` refers to the latency experienced by a delay-sensitive flow in case of parallel download and upload streams.
* `13-Wireless` refers to a flow completion time comparision between Ethernet and Wi-Fi.

Refer to the main [GitHub repository](https://github.com/richiMarchi/latency-tester) for the source code of the client
and server components used to perform the measurements.
