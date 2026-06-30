# hash:sha256:c1b5660ec0f6aaf28591d7731a553e89007e487426708ea0d8c51359d5d1a78f
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:2.5.2_cuda-11.2.2

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.8.1 \
    spikeinterface[full]==0.104.7
