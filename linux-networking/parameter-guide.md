# 参数决策表：有证据再修改

本文列出检查方向，不给通用推荐数值。具体可用项和语义以运行内核、驱动及本机手册为准。

| 参数或机制 | 什么证据支持研究它 | 可能代价 | 验证与恢复 |
| --- | --- | --- | --- |
| tcp_rmem / tcp_wmem | 长 RTT、窗口受限且端点可继续供数 | 每连接内存与排队 | 记录原三元组，新连接复测 |
| rmem_max / wmem_max | 应用请求缓冲受系统上限约束 | 总内存预算增长 | 核对实际 socket 值，恢复原上限 |
| somaxconn / 应用 listen backlog | 完成握手后的监听队列压力 | 更多等待连接，未必改善服务能力 | 结合应用 backlog、错误和接收速度 |
| tcp_max_syn_backlog | 半连接阶段压力证据 | 状态内存 | 区分半连接与已完成队列 |
| netdev_max_backlog | 软件接收积压相关丢弃 | 延迟与内存 | 排除应用慢，比较丢弃及尾延迟 |
| netdev_budget / netdev_budget_usecs | 软中断处理窗口不足的证据 | CPU 公平性与调度影响 | 看每核/应用延迟，恢复原值 |
| NIC ring size | 队列短时耗尽 | 缓冲占用与等待 | 实际支持范围、丢包、恢复原 ring |
| interrupt coalescing | 中断开销较高 | 延迟与低流量响应 | 记录 adaptive 状态与全部改动字段 |
| GRO/GSO/TSO | 特定工作负载或兼容性问题 | 关闭后 CPU/PPS 压力增大 | 一次一个特性，查询实际状态 |
| IRQ/CPU affinity | 跨 NUMA 或局部热点证据 | 同核竞争、配置维护 | 保存每个 IRQ 映射和服务状态 |
| nf_conntrack_max | 状态表容量压力 | 内存与查找开销 | 看 count/max 与失败统计，不只扩容 |

## 操作记录模板

1. 参数路径、当前值、来源版本、作用范围（主机/namespace/socket/设备）。
2. 预计改变哪项指标，何种结果意味着假设错误。
3. 测试值、持续时间、停止条件和恢复命令。
4. 当前值是否可能被 NetworkManager、systemd、irqbalance 或编排系统覆盖。
5. 临时变更通过验证后，再讨论持久化位置；不要一开始就修改系统启动配置。

参考：[IP sysctl](https://docs.kernel.org/networking/ip-sysctl.html)、[Conntrack sysctl](https://www.kernel.org/doc/html/latest/networking/nf_conntrack-sysctl.html)、[网卡案例文档 ixgbe](https://docs.kernel.org/networking/device_drivers/ethernet/intel/ixgbe.html)。
