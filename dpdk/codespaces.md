# GitHub Codespaces DPDK 学习环境

## 一键创建

打开 [创建 Codespace](https://codespaces.new/zhihaoevans/network-performance)，使用 main 分支与仓库提供的 devcontainer。首次创建会下载依赖并从源代码编译 DPDK；等待容器构建和 post-create 自检完成。

已有 Codespace：先保存工作并拉取 main，再从命令面板执行 **Codespaces: Rebuild Container**。仅 git pull 不会重建镜像中的软件。

当前连接工具只能提交配置，不能代替你创建/启动 Codespace。本文不表示实例已经运行。

## 预置内容

| 项目 | 配置 |
| --- | --- |
| 系统 | Ubuntu 24.04 devcontainer，vscode 用户 |
| DPDK | 24.11.7，固定源码 commit |
| 编译 | GCC、Meson、Ninja、pkg-config，debugoptimized |
| 调试 | GDB、Clang/clangd、Python |
| 网络工具 | iproute2、ethtool、iperf3、tcpdump、numactl、sysstat |
| PMD | null、pcap、ring、tap、af_packet，及必要基础驱动 |
| 官方样例 | helloworld、l2fwd |
| 仓库样例 | EAL/mempool/mbuf 生命周期程序 |
| 自检 | helloworld → mbuf 归还 → NULL PMD 非零 RX |

源代码位置：`/opt/dpdk-src`；构建目录：`/opt/dpdk-src/build`；安装前缀：`/opt/dpdk`。固定 commit 为 `6aa03946d205afca4c21b78c0d8a10d77389b132`，构建时核对 tag 实际指向，防止静默漂移。基础镜像与 apt 包仍随上游更新，非完全位级复现。

## 首次验收

```bash
cat /opt/dpdk/BUILD_INFO
pkg-config --modversion libdpdk
cat .local/dpdk-hello.log
cat .local/dpdk-mbuf.log
cat .local/dpdk-null.log
```

post-create 使用严格失败退出：任一步失败就停止，不会输出“自检通过”。若创建时失败，先查看对应日志；修复后可重新运行：

```bash
bash .devcontainer/post-create.sh
```

## 三个练习

### 1. EAL 与线程

```bash
python3 scripts/dpdk_lab.py hello
```

启动器从当前进程允许的 CPU 集合选择 CPU，并把 EAL lcore 0 映射过去，避免云容器 CPU 编号不是从 0 开始的问题。

### 2. mbuf 与 mempool

```bash
make -C examples/dpdk-mbuf
python3 scripts/dpdk_lab.py mbuf
```

查看并修改[示例代码](../examples/dpdk-mbuf/main.c)。预期打印 payload 和对象池恢复检查，不发送网络流量。

### 3. testpmd 虚拟端口

```bash
python3 scripts/dpdk_lab.py null
```

进入 testpmd 后：

```text
show port info all
show config fwd
start
stop
show port stats all
quit
```

start 后等待片刻再 stop。或执行有界自动检查：

```bash
python3 scripts/dpdk_lab.py null --smoke
```

NULL PMD 生成虚拟包并回收发送包。包计数用于验证执行路径，不能当作真实 NIC 吞吐或业务正确性结果。

## 为什么不配置 hugepages/VFIO

默认启动使用 `--no-huge --no-pci --no-shconf --iova-mode=va`，无需预留大页、挂载 hugetlbfs 或解绑系统网卡。此模式不支持 secondary process 共享实验，也不能用于验证依赖物理 DMA 的 PMD。

Codespaces 是 VM 上的开发容器。本配置不假定拥有可直通 NIC、硬件 RSS、可靠物理 NUMA 拓扑或专用发包器。真实网卡线速、硬件卸载、VFIO 与驱动研究转到专用 Linux 主机，见 [LAB-005](../labs/005-dpdk-forwarding.md)。

TAP/AF_PACKET PMD 虽已编译，其实时网络实验可能需要额外设备或权限，本配置不自动创建 TAP、不启用 privileged、不修改宿主网络。namespace/netem 实验也不作为默认验收项。

## 开发与持久化

重新编译 DPDK：

```bash
ninja -C /opt/dpdk-src/build -j 2
meson install -C /opt/dpdk-src/build
```

代码改在 /opt/dpdk-src 时，容器重建会丢失这些改动。长期成果应保存为仓库内的示例或补丁并提交；/workspaces 中的未提交修改也应主动备份/提交。不要把整个 DPDK 源码复制进本知识库。

## 常见问题

| 问题 | 处理 |
| --- | --- |
| apt/git 下载失败 | 查看构建日志，网络恢复后重建；不要跳过 commit 核验 |
| dpdk-testpmd 不存在 | 构建未完成或用了旧容器，重建后检查 /opt/dpdk/bin |
| CPU affinity 错误 | 使用启动器，不硬编码 -l 0-1 |
| 只有一个允许 CPU | hello/mbuf 可运行，NULL 转发需至少两个逻辑 CPU |
| hugepage/PCI 报错 | 检查是否绕开启动器或额外加了不匹配 EAL 选项 |
| NULL 自检 RX 为零 | 看 .local/dpdk-null.log、PMD 是否加载及配置是否完成 |
| 编译内存不足 | 保持 -j 2，检查 Codespace 可用内存 |
| perf 不能使用 | 取决于宿主内核与权限，不自动修改宿主设置 |

最低规格配置为 2 CPU / 8 GB。运行与存储使用受 GitHub 额度和计费规则约束，用完通过 Codespaces 菜单停止实例，不只关闭浏览器标签页；本仓库不设置自动扩容或自动启动。

## 本次验证范围

已核对固定版本源码中的构建选项，执行启动器逻辑测试、文档检查和 Shell 语法检查。当前执行环境没有 Docker/DPDK，尚未实际构建此镜像或在 Codespaces 中运行；完整验收由首次启动时的 post-create 检查完成。

参考：[GitHub devcontainer](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)、[DPDK 编译](https://doc.dpdk.org/guides-24.11/linux_gsg/build_dpdk.html)、[EAL 参数](https://doc.dpdk.org/guides-24.11/linux_gsg/linux_eal_parameters.html)、[NULL PMD](https://doc.dpdk.org/guides-24.11/nics/null.html)。在线 24.11 文档可能已跟随更新的补丁版，源码 commit 才是本环境基准。
