#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "apply-templates.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM ubuntu:focal AS downloader

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
	apt-get update; \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		ca-certificates \
		gnupg dirmngr \
		wget \
		xz-utils \
		\
		patch \
	; \
	tarball="$(basename "https://download.qemu.org/qemu-4.1.1.tar.xz")"; \
	wget -O "$tarball.sig" "https://download.qemu.org/qemu-4.1.1.tar.xz.sig"; \
	wget -O "$tarball" "https://download.qemu.org/qemu-4.1.1.tar.xz" --progress=dot:giga; \
	\
	export GNUPGHOME="$(mktemp -d)"; \
	for key in $QEMU_KEYS; do \
		gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
	done; \
	gpg --batch --verify "$tarball.sig" "$tarball"; \
	\
	mkdir /usr/src/qemu; \
	tar -xf "$tarball" -C /usr/src/qemu --strip-components=1; \
	\
	cd /usr/src/qemu; \
	\
	for p in /qemu-patches/*.patch; do \
		patch --strip 1 --input "$p"; \
	done; \
	ls -lashi /usr/src/qemu

FROM ubuntu:focal AS builder

COPY --from=downloader /usr/src/ /usr/src/

RUN set -eux; \
	cd /usr/src/qemu; \
	apt-get update; \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
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
	./configure --help; \
	CONFIGURE_EXTRA_OPTIONS=""; \
	if [ "`echo 4.1.1 | cut -c1-3`" = '5.1' ]; then \
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
		--disable-git-update \
		--disable-gtk \
		--disable-pvrdma \
		--disable-qed \
		--disable-sdl \
		--disable-vte \
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
	find /usr/local \
		-type f \
		\( -executable -o -name '*.so' \) \
		-exec sh -c 'test "$(head -c 2 "$1")" != "#!"' sh '{}' ';' \
		-exec ldd '{}' ';' \
			| awk '/=>/ { print $(NF-1) }' \
			| sort -u \
			| xargs -r basename -a \
			| xargs -r dpkg-query --search \
			| cut -d: -f1 \
			| sort -u > /usr/local/pkglist

FROM ubuntu:focal

COPY --from=builder /usr/local/ /usr/local/

RUN set -eux; \
	apt-get update; \
	export DEBIAN_FRONTEND=noninteractive ;\
	apt-get install -y --no-install-recommends \
		ovmf \
		netcat \
	; \
	xargs --arg-file=/usr/local/pkglist apt-get install -y --no-install-recommends; \
	rm -rf \
		/var/lib/apt/lists/* \
		/tmp/* \
		/var/cache/* \
		/var/tmp/* \
		/var/log/* \
	; \
# basic smoke test
	qemu-img --version

COPY start-qemu /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/start-qemu"]
