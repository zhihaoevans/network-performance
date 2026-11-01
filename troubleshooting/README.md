# 按症状排查

| 症状 | 入口 | 第一轮证据 |
| --- | --- | --- |
| 吞吐量达不到预期 | [吞吐瓶颈](throughput.md) | 实际发送、接收、每核、RTT |
| 丢包或重传增长 | [分层丢包](packet-loss.md) | 两端/网卡/协议/socket 增量 |
| P99、抖动或偶发卡顿 | [尾延迟](latency.md) | 时间窗口、失败率、排队与节流 |
| 单核忙而总体空闲 | [队列与亲和性](../linux-networking/queues-and-affinity.md) | 流到队列、IRQ、应用映射 |
| DPDK 加核不提速 | [多核扩展](../dpdk/multicore-and-detection.md) | 流偏斜、共享状态、跨 NUMA |
| 容器比宿主机慢 | [虚拟网络](../virtualization/container-networking.md) | 实际路径、CPU 配额、MTU |

排障顺序：确认复现条件 → 同窗口收集证据 → 排除测量问题 → 提出一个假设 → 单变量验证 → 恢复基线 → 写复盘。下面的候选原因均不是远程诊断结论。
