# hash:sha256:f2d99df18926a43e71387a9f5ed92809343d80b88d4445f281f90275452f3d66
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:0.2.0

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==1.0.0 \
    spikeinterface[full]==0.101.0

COPY postInstall /
RUN /postInstall
