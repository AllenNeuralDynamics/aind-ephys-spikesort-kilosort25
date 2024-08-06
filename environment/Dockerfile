<<<<<<< HEAD
# hash:sha256:0af88beeec2b7b403adb46b7123d3ea199873a1a513cb5fe05715d2104492e70
=======
# hash:sha256:fb7afeda8aa26c1c5ac8dfa6d8d313603356bd524cdab52a491082e9a25d77be
>>>>>>> 8ad5241757e02effa84a05c5022b17cde01eadff
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/kilosort2_5-compiled-base:0.2.0

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==0.38.0 \
<<<<<<< HEAD
    spikeinterface[full]==0.101.0
=======
    numpy==1.26.4 \
    spikeinterface[full]==0.100.7
>>>>>>> 8ad5241757e02effa84a05c5022b17cde01eadff
