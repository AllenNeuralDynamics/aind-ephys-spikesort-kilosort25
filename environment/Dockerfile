FROM spikeinterface/kilosort2_5-compiled-base:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nvidia-cuda-toolkit=9.1.85-3ubuntu1 \
        nvidia-driver-510=510.108.03-0ubuntu0.18.04.1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U --no-cache-dir \
    aind-data-schema==0.22.1 \
    spikeinterface[full]==0.99.1
