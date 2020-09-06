# tlex/docker-qemu

This is a fork of [tianon/docker-qemu](https://github.com/tianon/docker-qemu).

Notable differences, beyond the automated build using GitLab CI:

* Uses `ubuntu:focal` instead of `debian:buster-slim`
* Adds support for RBD (CEPH) volumes
* Adds support for SPICE

## Supported tags

* `4.1.1`, `4.1`
* `4.2.1`, `4.2`
* `5.0.0`, `5.0`
* `5.1.0`, `5.1`, `latest`

## Usage

This image is hosted on registry.gitlab.com:
```
registry.gitlab.com/tlex/docker-qemu:latest
```

### Examples
Create a new RBD volume:

```sh
sudo docker run --rm -it \
  -v /etc/ceph/ceph.conf:/etc/ceph/ceph.conf:ro \
  -v /etc/ceph/ceph.client.qemu.keyring:/etc/ceph/ceph.client.qemu.keyring:ro \
  registry.gitlab.com/tlex/docker-qemu:latest \
    qemu-img create -f raw rbd:rbd/desktop:id=qemu 100G
```

Start an image with an RBD volume and QXL graphics driver:
```sh
sudo docker run --rm -it \
  --device /dev/kvm \
  -v /etc/ceph/ceph.conf:/etc/ceph/ceph.conf:ro \
  -v /etc/ceph/ceph.client.qemu.keyring:/etc/ceph/ceph.client.qemu.keyring:ro \
  -v /docker/mini.iso:/tmp/mini.iso \
  tianon/qemu:latest \
        qemu-system-x86_64 \
          -enable-kvm \
          -smp 4 \
          -m 8192 \
          -boot order=d \
          -device virtio-scsi-pci \
          -drive format=rbd,file=rbd:rbd/desktop:id=qemu,id=drive1,cache=writeback,if=none \
          -device driver=scsi-hd,drive=drive1,discard_granularity=512 \
          -netdev user,hostname=desktop,hostfwd=tcp::22-:22,id=net \
          -device virtio-net-pci,netdev=net \
          -serial stdio \
          -vnc :0 \
          -no-user-config \
          -cpu host \
          -nodefaults \
          -vga qxl \
          -cdrom /tmp/mini.iso
```

The original `start-qemu` script is still included, from [tianon/docker-qemu](https://github.com/tianon/docker-qemu). Please read below for detail.

___

Original README content below:

# tianon/qemu

	touch /home/jsmith/hda.qcow2
	docker run -it --rm \
		--device /dev/kvm \
		--name qemu-container \
		-v /home/jsmith/hda.qcow2:/tmp/hda.qcow2 \
		-e QEMU_HDA=/tmp/hda.qcow2 \
		-e QEMU_HDA_SIZE=100G \
		-e QEMU_CPU=4 \
		-e QEMU_RAM=4096 \
		-v /home/jsmith/downloads/debian.iso:/tmp/debian.iso:ro \
		-e QEMU_CDROM=/tmp/debian.iso \
		-e QEMU_BOOT='order=d' \
		-e QEMU_PORTS='2375 2376' \
		tianon/qemu

Note: port 22 will always be mapped (regardless of the contents of `QEMU_PORTS`).

For supplying additional arguments, use a command of `start-qemu <args>`. For example, to use `-curses`, one would `docker run ... tianon/qemu start-qemu -curses`.

For UEFI support, [the `ovmf` package](https://packages.debian.org/sid/ovmf) is installed, which can be utilized most easily by supplying `--bios /usr/share/ovmf/OVMF.fd`.
