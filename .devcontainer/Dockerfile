FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG DPDK_TAG=v24.11.7
ARG DPDK_COMMIT=6aa03946d205afca4c21b78c0d8a10d77389b132

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential meson ninja-build pkg-config python3 python3-pyelftools \
    python3-venv libnuma-dev libpcap-dev git ca-certificates \
    gdb clang clangd make iproute2 iputils-ping ethtool iperf3 \
    numactl tcpdump sysstat pciutils procps jq \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch "${DPDK_TAG}" \
      https://github.com/DPDK/dpdk-stable.git /opt/dpdk-src \
    && test "$(git -C /opt/dpdk-src rev-parse HEAD)" = "${DPDK_COMMIT}" \
    && meson setup /opt/dpdk-src/build /opt/dpdk-src \
      --prefix=/opt/dpdk --libdir=lib --buildtype=debugoptimized \
      -Dplatform=generic -Dtests=false -Denable_docs=false \
      -Denable_apps=test-pmd \
      -Denable_drivers=net/null,net/pcap,net/ring,net/tap,net/af_packet \
      -Dexamples=helloworld,l2fwd \
    && ninja -C /opt/dpdk-src/build -j 2 \
    && meson install -C /opt/dpdk-src/build \
    && printf '%s\n' /opt/dpdk/lib > /etc/ld.so.conf.d/dpdk.conf \
    && ldconfig \
    && printf 'tag=%s\ncommit=%s\n' "${DPDK_TAG}" "${DPDK_COMMIT}" > /opt/dpdk/BUILD_INFO \
    && chown -R vscode:vscode /opt/dpdk-src /opt/dpdk

ENV PATH="/opt/dpdk/bin:${PATH}" \
    PKG_CONFIG_PATH="/opt/dpdk/lib/pkgconfig" \
    DPDK_SOURCE="/opt/dpdk-src"
