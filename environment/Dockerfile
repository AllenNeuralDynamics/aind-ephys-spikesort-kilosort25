# hash:sha256:b564b89084238a38ce4f7cf9c909d6781a291894a666f0bc6b2b1d5596bc77b4
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:2.5.2_cuda-11.2.2

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.4.0 \
    spikeinterface[full]==0.103.0
