# hash:sha256:c1e12fea50653e2ecc4b4b96cff6bb0971a1f2e1cbfc473c244f0201a537c441
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:0.2.0

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==0.38.0

COPY postInstall /
RUN /postInstall
