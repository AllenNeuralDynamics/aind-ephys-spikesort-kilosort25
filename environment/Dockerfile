# hash:sha256:cf1e75e6cc870bac05723e9fbbdeb8617f59be10bc2e1a473a0c9137d7452ec5
FROM registry.codeocean.allenneuraldynamics.org/codeocean/kilosort2_5-compiled-base:latest

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==0.13.50

COPY postInstall /
RUN /postInstall
