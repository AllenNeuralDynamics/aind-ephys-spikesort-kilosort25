# hash:sha256:4470eb464d287478216dbceb5d5bd81cdc09a9461f7ee6cb0fb1d955304145e2
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:2.5.2_cuda-11.2.2

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.8.1 \
    log-schema==0.2.10.dev1 \
    spikeinterface[full]==0.105.0
