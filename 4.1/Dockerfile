#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "apply-templates.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM ubuntu:focal

RUN apt-get update && apt-get install -y --no-install-recommends \
		ovmf \
		netcat \
	&& rm -rf /var/lib/apt/lists/*

COPY *.patch /qemu-patches/

# https://wiki.qemu.org/SecurityProcess
ENV QEMU_KEYS \
# Michael Roth
		CEACC9E15534EBABB82D3FA03353C9CEF108B584
# https://wiki.qemu.org/Planning/ReleaseProcess#Sign_the_resulting_tarball_with_GPG: (they get signed by whoever is making the release)

# https://www.qemu.org/download/#source
# https://download.qemu.org/?C=M;O=D
ENV QEMU_VERSION 4.1.1
ENV QEMU_URL https://download.qemu.org/qemu-4.1.1.tar.xz

RUN set -eux; \
	\
	savedAptMark="$(apt-mark showmanual)"; \
	\
	apt-get update; \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		gnupg dirmngr \
		wget \
		xz-utils \
		\
		patch \
		\
		bzip2 \
		gcc \
		gnutls-dev \
		libaio-dev \
		libbz2-dev \
		libc-dev \
		libcap-dev \
		libcap-ng-dev \
		libcurl4-gnutls-dev \
		libglib2.0-dev \
		libiscsi-dev \
		libjpeg-dev \
		liblzo2-dev \
		libncursesw5-dev \
		libnfs-dev \
		libnuma-dev \
		libpixman-1-dev \
		libpng-dev \
		librbd-dev \
		libseccomp-dev \
		libssh-dev \
		libusb-1.0-0-dev \
		libusbredirparser-dev \
		make \
		pkg-config \
		python \
		xfslibs-dev \
		zlib1g-dev \
	; \
	rm -rf /var/lib/apt/lists/*; \
	\
	tarball="$(basename "$QEMU_URL")"; \
	wget -O "$tarball.sig" "$QEMU_URL.sig"; \
	wget -O "$tarball" "$QEMU_URL" --progress=dot:giga; \
	\
	export GNUPGHOME="$(mktemp -d)"; \
	for key in $QEMU_KEYS; do \
		gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
	done; \
	gpg --batch --verify "$tarball.sig" "$tarball"; \
	gpgconf --kill all; \
	rm -rf "$GNUPGHOME"; \
	\
	mkdir /usr/src/qemu; \
	tar -xf "$tarball" -C /usr/src/qemu --strip-components=1; \
	rm "$tarball" "$tarball.sig"; \
	\
	cd /usr/src/qemu; \
	\
	for p in /qemu-patches/*.patch; do \
		patch --strip 1 --input "$p"; \
	done; \
	rm -rf /qemu-patches; \
	\
	./configure --help; \
	CONFIGURE_EXTRA_OPTIONS=""; \
	if [ "`echo $QEMU_VERSION | cut -c1-3`" = '5.1' ]; then \
		export CONFIGURE_EXTRA_OPTIONS=" --enable-rng-none" ;\
	fi; \
	./configure \
		--extra-cflags="-O2 -pipe -fomit-frame-pointer" \
		--target-list=' \
# system targets
			i386-softmmu x86_64-softmmu aarch64-softmmu arm-softmmu \
			mips64-softmmu mips64el-softmmu ppc64-softmmu \
			sparc64-softmmu \
		' \
		--disable-docs \
		--disable-gtk --disable-vte \
		--disable-sdl \
		--disable-xen \
		--enable-attr \
		--enable-bzip2 \
		--enable-cap-ng \
		--enable-curl \
		--enable-curses \
		--enable-fdt \
		--enable-gnutls \
		--enable-guest-agent \
		--enable-kvm \
		--enable-libiscsi \
		--enable-libnfs \
		--enable-libssh \
		--enable-libusb \
		--enable-linux-aio \
		--enable-linux-user \
		--enable-lzo \
		--enable-modules \
		--enable-numa \
		--enable-rbd \
		--enable-seccomp \
		--enable-system \
		--enable-tools \
		--enable-usb-redir \
		--enable-vhost-net \
		--enable-vhost-user \
		--enable-vhost-vsock \
		--enable-virtfs \
		--enable-vnc \
		--enable-vnc-jpeg \
		--enable-vnc-png \
		--enable-xfsctl \
		$CONFIGURE_EXTRA_OPTIONS \
	; \
	make -j "$(nproc)"; \
	make install; \
	\
	cd /; \
	rm -rf /usr/src/qemu; \
	\
	apt-mark auto '.*' > /dev/null; \
	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; \
	find /usr/local \
		-type f \
		\( -executable -o -name '*.so' \) \
		-exec ldd '{}' ';' \
			| awk '/=>/ { print $(NF-1) }' \
			| sort -u \
			| xargs -r basename -a \
			| xargs -r dpkg-query --search \
			| cut -d: -f1 \
			| sort -u \
			| xargs -r apt-mark manual \
	; \
	apt-get purge -y --auto-remove; \
	\
# basic smoke test
	qemu-img --version

COPY start-qemu /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/start-qemu"]
