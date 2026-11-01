# LAB-004：队列分布与 NUMA 局部性

状态：待执行；需要多队列网卡，NUMA 部分需要可见多节点拓扑。单节点环境只做分流观察。

## 目标与前提

从“单流是否集中”“增加流数是否分散”“本地内存是否影响表现”三个问题分别建立实验。不要同时改变流数、队列数和内存位置。

## 步骤

1. 保存 ethtool -l/-x/-S、/proc/interrupts、CPU 拓扑和网卡节点。
2. 固定总 offered load，分别用单流和多流；确认源/目的字段确实变化。
3. 比较 per-queue 和 per-core 增量，记录热点位置。
4. 保持设备配置，用 numactl 的 --cpunodebind/--membind 为新启动应用选择已有节点；先确认可用内存与 cpuset 限制。
5. 比较本地与远端放置，每次重新启动并确认实际内存位置。
6. 若要研究 IRQ/队列数量，另开配置组，保存映射和恢复步骤。

## 验收

给出流—队列—CPU 映射，说明是否存在单流或重流瓶颈。报告吞吐、P99（如可测）、CPU 与跨节点放置，而不是只报告启动参数。

## 恢复

进程级 numactl 策略随进程退出结束；已修改的 IRQ、队列、RSS 和 irqbalance 状态必须单独恢复。重新查询原配置并复跑基线。

关联：[NUMA](../nic-and-hardware/numa-and-memory.md)、[队列](../linux-networking/queues-and-affinity.md)。
