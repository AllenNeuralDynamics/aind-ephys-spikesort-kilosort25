# hash:sha256:4340e0412522774da98cc81eefc63f384cd55431eae0874beb2f8dad14de15d5
FROM registry.codeocean.allenneuraldynamics.org/codeocean/kilosort2_5-compiled-base:latest

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nvidia-cuda-toolkit=9.1.85-3ubuntu1 \
        nvidia-driver-510=510.108.03-0ubuntu0.18.04.1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U --no-cache-dir \
    aind-data-schema==0.15.25

COPY postInstall /
RUN /postInstall
