# NUMA、缓存与内存布局

## 观察三种位置

性能关键的是网卡所在节点、处理线程所在 CPU，以及包缓冲/状态表实际分配的位置。只绑定线程，不意味着已经分配的内存自动迁移。

```bash
IFACE=eth0
lscpu
numactl --hardware
cat "/sys/class/net/$IFACE/device/numa_node"
readlink -f "/sys/class/net/$IFACE/device"
```

虚拟接口可能没有 device，numa_node 为 -1 表示位置未知而不是节点 -1。虚拟机暴露的拓扑也不一定反映物理硬件。

## 设计对比

| 组别 | 线程 | 内存 | 目的 |
| --- | --- | --- | --- |
| A | 与网卡同节点 | 同节点 | 局部性基线 |
| B | 另一节点 | 另一节点 | 对比远端 I/O 路径 |
| C | 同节点 | 另一节点 | 单独观察内存位置 |
| D | 同节点 | 同节点，增加工作核 | 观察扩展与共享竞争 |

各组重启应用以重新控制分配策略；记录实际放置，不仅记录启动参数。cgroup cpuset 限制可能覆盖程序希望使用的节点范围。

## 热路径布局

把频繁一起访问的数据放近，把不同核频繁写入的计数器分开。对共享状态考虑分片、只读副本与批量更新，同时明确一致性语义。

不能只凭结构体加 padding 就声称性能改善。比较实际 cache miss、CPU cycles、吞吐与内存占用，并确认缓存行大小和编译布局。

## HugeTLB 与 TLB

大页减少特定工作集的地址转换压力，但需要资源规划；显式 HugeTLB 与透明大页不是同一机制。大页不足、节点分配错误或内存锁定限制可能先成为启动问题。记录每节点页大小、总量、空闲量和应用实际用量。

参考：[NUMA Memory Policy](https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html)、[HugeTLB](https://docs.kernel.org/admin-guide/mm/hugetlbpage.html)。实践：[队列/NUMA 实验](../labs/004-queues-numa.md)。
