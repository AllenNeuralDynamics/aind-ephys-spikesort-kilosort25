# hash:sha256:4340e0412522774da98cc81eefc63f384cd55431eae0874beb2f8dad14de15d5
FROM registry.codeocean.allenneuraldynamics-test.org/codeocean/kilosort2_5-compiled-base:latest

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN conda install -y \
        jupyterlab==4.2.5 \
    && conda clean -ya

RUN pip install -U --no-cache-dir \
    aind-data-schema==1.0.0 \
    spikeinterface[full]==0.101.1

COPY postInstall /
RUN /postInstall
