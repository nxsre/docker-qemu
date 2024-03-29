[![Pipeline Status](https://gitlab.com/ix.ai/docker-qemu/badges/master/pipeline.svg)](https://gitlab.com/ix.ai/docker-qemu/)
[![Docker Stars](https://img.shields.io/docker/stars/ixdotai/qemu.svg)](https://hub.docker.com/r/ixdotai/qemu/)
[![Docker Pulls](https://img.shields.io/docker/pulls/ixdotai/qemu.svg)](https://hub.docker.com/r/ixdotai/qemu/)
[![Docker Image Version (latest)](https://img.shields.io/docker/v/ixdotai/qemu/latest)](https://hub.docker.com/r/ixdotai/qemu/)
[![Docker Image Size (latest)](https://img.shields.io/docker/image-size/ixdotai/qemu/latest)](https://hub.docker.com/r/ixdotai/qemu/)
[![Gitlab Project](https://img.shields.io/badge/GitLab-Project-554488.svg)](https://gitlab.com/ix.ai/docker-qemu/)

# ix.ai/docker-qemu

Notable features, beyond the automated build using GitLab CI:

* Multi-arch build: `linux/amd64`, `linux/arm64`, `linux/arm/v7`, `linux/386`
* Full support for RBD (CEPH) volumes - including libraries
* Enabled `rng-none`
* No additional signal patches needed, by using QMP to gracefully shut down the VM on container stop (with `system_powerdown`)

## Supported tags

* `7.1`
* `7.2`, `latest`

The simple `N.N.N` tags refer to the QEMU versions.

## Usage

This image is hosted on docker hub and gitlab registry:

```
ixdotai/qemu:latest
registry.gitlab.com/ix.ai/docker-qemu:latest
```

### Examples

Create a new RBD volume:

```sh
sudo docker run --rm -it \
  -v /etc/ceph/ceph.conf:/etc/ceph/ceph.conf:ro \
  -v /etc/ceph/ceph.client.qemu.keyring:/etc/ceph/ceph.client.qemu.keyring:ro \
  --entrypoint "" \
  ixdotai/qemu:latest \
    qemu-img create -f raw rbd:rbd/desktop:id=qemu 100G
```

Start an image with an RBD volume, boot from the ISO:

```sh
sudo docker run --rm -it \
  --device /dev/kvm \
  -v /etc/ceph/ceph.conf:/etc/ceph/ceph.conf:ro \
  -v /etc/ceph/ceph.client.qemu.keyring:/etc/ceph/ceph.client.qemu.keyring:ro \
  -v /docker/mini.iso:/tmp/mini.iso \
  ixdotai/qemu:latest \
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
    -vga virtio \
    -cdrom /tmp/mini.iso
```

## Global Variables

The following variables are supported for all operations type:

| **Variable**             | **Default**           | **Description**                                 |
|:-------------------------|:---------------------:|:------------------------------------------------|
| `QEMU_NO_QMP`            | -                     | Set this to anything to disable the QMP Monitor **and** graceful shutdown handling |
| `QEMU_MONPORT`           | `7100`                | The port for the QMP Monitor |
| `QEMU_POWERDOWN_TIMEOUT` | `120`                 | After this many seconds, the VM gets killed after a graceful shutdown command |
| `QEMU_ARCH`              | output of `uname -m`  | Allows starting the VM with a different arch than the host. Supported: `i386`, `x86_64`, `aarch64`, `arm`, `mips64`, `mips64el`, `ppc64`, `sparc64` |
| `DEBUG_SCRIPT`           | `false`               | Set this to `true`, to have all de debug log of the script controlling the container. **WARNING!** This will generate a few log lines per second! |

## Tips

### Variable inside the VMs

To add a string from outside the VM to be visible inside (for example, a host id), I'm using:

```
-smbios type=1,serial=alpine
```

I'm then reading this inside the VM with `dmidecode --string system-serial-number`

For more details, see this [gist](https://gist.github.com/smoser/290f74c256c89cb3f3bd434a27b9f64c).

### Mount a volume from the docker host inside the VM

This is only possible by exposing a FAT drive.

Let's say the volume on the docker host is `/files`.

You need to add the following to the `docker run` command:

```
  -v /files:/files:rw \
```

And in the VM command:

```
    -drive file=fat:rw:/folder,id=drive2,if=none,format=raw \
    -device driver=scsi-hd,drive=drive2 \
```

When you start your VM, you will see an additional drive - if you add it after the RBD one, it will be `sdb` in Linux.

---

## Fork

This is a fork of [tianon/docker-qemu](https://github.com/tianon/docker-qemu).

Support for the original `start-qemu` script was still included at the time of the fork, from [tianon/docker-qemu](https://github.com/tianon/docker-qemu). If no arguments are
passed to the image, then the environment variables documented in [start-qemu](start-qemu) are used.

### Original README content below

#### tianon/qemu

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
