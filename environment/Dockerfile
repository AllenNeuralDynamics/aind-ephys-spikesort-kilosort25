# hash:sha256:303335bae4f4d7437ebf793af4b0ed2721f6ff60a57e781a60d9b8b9af1c3568
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:0.2.0

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.4.0 \
    spikeinterface[full]==0.103.0
