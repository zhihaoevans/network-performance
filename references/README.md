# 官方资料索引与版本说明

首次集中核对：2026-11-01。优先依据项目官方文档、Linux man-pages 和 RFC；工程排查表、实验矩阵与示例由本仓库组织，不是对来源的逐字转录。

## Linux

| 资料 | 用途 |
| --- | --- |
| [Scaling](https://docs.kernel.org/networking/scaling.html) | RSS/RPS/RFS/XPS |
| [NAPI](https://docs.kernel.org/networking/napi.html) | 网络事件处理 |
| [IP sysctl](https://docs.kernel.org/networking/ip-sysctl.html) | 协议栈参数语义 |
| [Interface statistics](https://docs.kernel.org/networking/statistics.html) | 计数器层次与来源 |
| [Segmentation offloads](https://docs.kernel.org/networking/segmentation-offloads.html) | TSO/GSO/GRO |
| [NUMA policy](https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html) | 内存策略与 cpuset |
| [HugeTLB](https://docs.kernel.org/admin-guide/mm/hugetlbpage.html) | 显式大页 |
| [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) | CPU 配额与资源隔离 |
| [Conntrack sysctl](https://www.kernel.org/doc/html/latest/networking/nf_conntrack-sysctl.html) | 状态表配置 |
| [ixgbe](https://docs.kernel.org/networking/device_drivers/ethernet/intel/ixgbe.html) | 特定驱动参考 |
| [AF_XDP](https://docs.kernel.org/networking/af_xdp.html) | UMEM 与 ring |
| [BPF](https://docs.kernel.org/bpf/index.html) | 验证器、BTF 与程序类型 |
| [MSG_ZEROCOPY](https://docs.kernel.org/networking/msg_zerocopy.html) | 复制规避和完成通知 |
| [Kernel TLS](https://docs.kernel.org/networking/tls.html) | TLS 数据路径 |
| [perf 数据与权限](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html) | 观测边界 |

## DPDK

| 资料 | 用途 |
| --- | --- |
| [Overview](https://doc.dpdk.org/guides/prog_guide/overview.html) | 组件与执行模型 |
| [PMD/ethdev](https://doc.dpdk.org/guides/prog_guide/ethdev/ethdev.html) | 队列与收发模型 |
| [Mbuf](https://doc.dpdk.org/guides/prog_guide/mbuf_lib.html) | 包对象 |
| [Mempool](https://doc.dpdk.org/guides/prog_guide/mempool_lib.html) | 对象池 |
| [Efficient code](https://doc.dpdk.org/guides/prog_guide/writing_efficient_code.html) | 内存与热路径 |
| [testpmd 启动](https://doc.dpdk.org/guides/testpmd_app_ug/run_app.html) | 参数格式 |
| [testpmd 运行](https://doc.dpdk.org/guides/testpmd_app_ug/testpmd_funcs.html) | 交互与统计 |
| [Ethdev API](https://doc.dpdk.org/api/rte__ethdev_8h.html) | 返回值、所有权与并发限制 |

DPDK 无版本路径在核对时显示 26.11.0-rc1。它是候选发布文档，不是仓库推荐版本；实际实验使用所安装 release/commit 对应的文档与 API，记录驱动、固件和编译选项。

## 传输协议与工具

| 资料 | 用途 |
| --- | --- |
| [RFC 6349](https://www.rfc-editor.org/rfc/rfc6349.html) | TCP 吞吐测试框架，信息性 RFC |
| [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html) | TCP 规范 |
| [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html) | QUIC 恢复与拥塞控制 |
| [iperf3](https://software.es.net/iperf/invoking.html) | 测试选项和端点口径 |
| [tcp(7)](https://man7.org/linux/man-pages/man7/tcp.7.html) | Linux TCP 接口 |
| [udp(7)](https://man7.org/linux/man-pages/man7/udp.7.html) | UDP 行为 |
| [epoll(7)](https://man7.org/linux/man-pages/man7/epoll.7.html) | 事件模型 |
| [recvmmsg(2)](https://man7.org/linux/man-pages/man2/recvmmsg.2.html) | 批量接收 |
| [tc-netem(8)](https://man7.org/linux/man-pages/man8/tc-netem.8.html) | 网络条件模拟 |

网页版本可能不同于本机版本。遇到冲突时优先核对实际二进制帮助、发行版补丁和相应源码，不把在线 latest 直接当成运行环境事实。

## 补充主题

- [Linux Timestamping](https://docs.kernel.org/networking/timestamping.html)：时间戳来源与接口。
- [ipv6(7)](https://man7.org/linux/man-pages/man7/ipv6.7.html)：Linux IPv6 API。
- [NVIDIA RDMA Programming Manual v1.7](https://docs.nvidia.com/rdma-aware-networks-programming-user-manual-1-7.pdf)：RDMA 基础资源与操作，不作最新设备配置手册。
