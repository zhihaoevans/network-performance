# 硬件与 DPDK 术语

[返回概念索引](README.md)

## 硬件与内存

| 术语 | 英文 | 定义与性能意义 |
| --- | --- | --- |
| NUMA | Non-Uniform Memory Access | 内存访问成本与 CPU、内存所在节点有关；应同时考虑网卡、线程和缓冲区位置。 |
| CPU 亲和性 | CPU Affinity | 约束线程或中断可运行的 CPU；绑定后仍需检查负载是否集中。 |
| 缓存行 | Cache Line | CPU 缓存一致性和数据传输的重要粒度；大小依体系结构而定。 |
| 缓存未命中 | Cache Miss | 访问未命中相应缓存层级，需要从其他层级取得数据。 |
| 伪共享 | False Sharing | 多核修改同一缓存行中的不同数据，产生不必要的一致性流量。 |
| DMA | Direct Memory Access | 设备与内存间传输数据的机制，不需要 CPU 逐字节复制；仍有映射与管理开销。 |
| PCIe | Peripheral Component Interconnect Express | 设备互连总线，速率、通道数和拓扑会影响 I/O 能力。 |
| 大页 | Huge Pages | 使用更大页粒度的内存映射，可降低某些地址转换开销，需考虑分配与管理代价。 |
| TLB | Translation Lookaside Buffer | 缓存地址转换结果的硬件结构；TLB miss 与数据 cache miss 不同。 |

## DPDK 核心对象

| 术语 | 英文 | 定义与注意事项 |
| --- | --- | --- |
| DPDK | Data Plane Development Kit | 面向高性能数据平面处理的库与驱动集合，不是完整 TCP/IP 栈。 |
| EAL | Environment Abstraction Layer | 提供启动、内存和执行环境等基础抽象。 |
| PMD | Poll Mode Driver | DPDK 驱动术语，网络数据路径常用轮询收发，具体能力依驱动而异。 |
| lcore | Logical Core | DPDK 管理执行线程的逻辑标识，不能一概视为物理核编号；需查看 CPU 映射。 |
| mbuf | rte_mbuf | 描述包数据、长度和元数据的对象；一个包可由多个 mbuf 段组成。 |
| mempool | Memory Pool | 可复用对象池；mbuf 通常从池中分配并在释放后归还。 |
| ring | rte_ring | 软件 FIFO，用于对象或消息传递；不是网卡硬件描述符环。 |
| descriptor | Descriptor | 设备队列中的工作描述条目，含缓冲区或控制信息；数量不必与包数一一对应。 |
| burst | Burst | 一次调用批量处理多个包；API 返回的实际数量可能小于请求上限。 |
| rte_flow | Flow API | 描述流匹配与动作的接口，支持范围由设备和驱动决定。 |

## 执行方式

| 术语 | 含义 | 需要观察的代价 |
| --- | --- | --- |
| Run-to-completion | 一个执行单元完成该包的一系列处理步骤 | 复杂逻辑和负载不均衡 |
| Pipeline | 不同执行单元负责不同阶段，通过队列传递工作 | 队列等待、跨核通信、缓存迁移 |
| Busy polling | 持续检查工作是否到达 | CPU 与功耗，空轮询占比 |
| Zero-copy | 在指定路径上避免某次数据复制 | 仍有所有权、生命周期和 DMA 等管理成本 |
| Lock-free | 满足非阻塞系统进展保证的算法性质 | 不代表无原子操作、无竞争或每线程等待有界 |

忙轮询线程显示高 CPU 使用率不代表它正在满负载处理业务包。判断能力上限仍需结合有效包速率、空轮询、丢包和延迟。

## 参考资料

- [DPDK Overview](https://doc.dpdk.org/guides/prog_guide/overview.html)：基础组件与执行模型。
- [DPDK Mbuf Library](https://doc.dpdk.org/guides/prog_guide/mbuf_lib.html)：包缓冲区与对象生命周期。
- [DPDK Glossary](https://doc.dpdk.org/guides/prog_guide/glossary.html)：官方缩写和术语。

上述 DPDK 在线文档在 2026-11-01 查阅时为 26.11.0-rc1；术语整理不构成对该版本的选型建议，复现实验应匹配实际安装版本。
