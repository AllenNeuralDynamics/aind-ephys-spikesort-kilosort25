# hash:sha256:744e5cd07d90213547b655cc1b27153f3fb28fa9d8687ae0f5fee5d4211301ca
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:0.2.0

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==1.3.0 \
    spikeinterface[full]==0.102.1
