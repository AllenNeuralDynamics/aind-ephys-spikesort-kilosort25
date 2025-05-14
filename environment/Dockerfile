# hash:sha256:7292dc3b849508de7267caf04bf3da96eaa5972accc698afc7247209ac82bb69
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:0.2.0

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==1.3.0 \
    spikeinterface[full]==0.102.3
