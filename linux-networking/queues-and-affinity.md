# 多队列、RSS/RPS/RFS/XPS 与 CPU 放置

## 选择路径

先画出“流 → RX 队列 → IRQ/NAPI CPU → 应用线程 → TX 队列”的映射。RSS 在网卡侧分流；RPS 在软件中选择接收处理 CPU；RFS 改善应用局部性；XPS 影响 TX 队列选择。机制可以组合，但组合不保证更快。

## 只读检查

```bash
IFACE=eth0  # 替换为被测接口
ethtool -l "$IFACE"
ethtool -x "$IFACE"
ethtool -S "$IFACE"
ls "/sys/class/net/$IFACE/queues"
cat /proc/interrupts
```

不支持某查询不等于硬件没有性能。要区分驱动 API 不支持、虚拟接口与权限问题。

## 对比实验

| 变量 | 固定条件 | 关键观察 |
| --- | --- | --- |
| 单流/多流 | 总 offered load、包长 | 队列分布与关键核 |
| 队列数量 | CPU 集合与总负载 | 每队列工作量、额外管理成本 |
| IRQ/应用同核或同 NUMA | 负载与内存位置 | 局部性与 CPU 竞争 |
| 软件分流开/关 | 硬件配置不变 | IPI、缓存迁移与总 CPU |

同流通常落在同一 RX 队列，因此增加队列不必然改善单流吞吐。哈希字段与封装也会影响分流效果。

## 修改前后

记录当前通道数、RSS 表、各队列 rps_cpus/rps_flow_cnt/xps_cpus、IRQ affinity 和 irqbalance 状态。队列数量变化可能重建 IRQ 和配置，不能只恢复一个整数就认定完整恢复。

不要将同一份 CPU 掩码照搬到所有机器。CPU 编号、SMT 兄弟与 NUMA 拓扑必须先确认。恢复后重新查询并复跑基线。

参考：[Linux Scaling](https://docs.kernel.org/networking/scaling.html)。实践：[队列与局部性实验](../labs/004-queues-numa.md)。
