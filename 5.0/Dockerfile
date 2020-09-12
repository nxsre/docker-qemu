#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "apply-templates.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM debian:stable-slim
LABEL maintainer="git@alex.thom.ae" \
      ai.ix.repository="gitlab.com/tlex/docker-qemu/"

# https://wiki.qemu.org/SecurityProcess
# Michael Roth
ENV QEMU_KEYS="CEACC9E15534EBABB82D3FA03353C9CEF108B584" \
		QEMU_VERSION="5.0.0" \
		QEMU_URL="https://download.qemu.org/qemu-5.0.0.tar.xz"

COPY *.patch /qemu-patches/

COPY build /usr/local/bin/

RUN /usr/local/bin/build

COPY start-qemu /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/start-qemu"]
