# hash:sha256:7a62d3b38825f43c9f5c8d7e1e38965e1c4d5d66309f02ef252ef64bd1bcbc1a
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:latest

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nvidia-cuda-toolkit=9.1.85-3ubuntu1 \
        nvidia-driver-510=510.108.03-0ubuntu0.18.04.1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.8.1 \
    spikeinterface[full]==0.104.7

COPY postInstall /
RUN --mount=type=secret,id=secrets . /run/secrets/secrets \
    && /postInstall
