#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "apply-templates.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM debian:bullseye-slim
LABEL maintainer="docker@ix.ai" \
      ai.ix.repository="ix.ai/docker-qemu"

# https://wiki.qemu.org/SecurityProcess
# Michael Roth
ENV QEMU_KEYS="CEACC9E15534EBABB82D3FA03353C9CEF108B584" \
		QEMU_BUILD_VERSION="8.0.3" \
		QEMU_URL="https://download.qemu.org/qemu-8.0.3.tar.xz"

COPY Dockerfile *.patch /qemu-patches/

COPY build start-qemu /usr/local/bin/

RUN /usr/local/bin/build

ENTRYPOINT ["/usr/local/bin/start-qemu"]
