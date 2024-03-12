# hash:sha256:c557263f1d1ec0ba93504ddb60334353802bb5b30f5bfcc610c6b9e519e874dc
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:0.3.0

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==0.19.1 \
    spikeinterface[full]==0.100.0
