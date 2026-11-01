# Linux 网络性能只读命令速查

变量 IFACE 设为被测接口，PID 设为被测进程。命令可能需要对应工具包或权限；不支持时记录原因，不为采集自动更改系统权限。

| 目的 | 命令 | 关注点 |
| --- | --- | --- |
| 系统/CPU | uname -a；lscpu | 版本、核与 NUMA 拓扑 |
| 地址与链路 | ip -br addr；ip -d link | 接口类型、MTU、隧道 |
| 路由 | ip route get DESTINATION | 实际出口、源地址 |
| 标准计数 | ip -s -s link show dev "$IFACE" | 包、字节、细分错误 |
| 驱动统计 | ethtool -S "$IFACE" | per-queue 与硬件错误 |
| 设备信息 | ethtool -i "$IFACE" | 驱动、固件、BDF |
| 队列/RSS | ethtool -l "$IFACE"；ethtool -x "$IFACE" | 队列数与分配 |
| offload | ethtool -k "$IFACE" | GRO/GSO/TSO 等 |
| 中断 | cat /proc/interrupts | IRQ 到 CPU 的分布 |
| 软中断 | cat /proc/softirqs | 各 CPU 的 NET_RX/NET_TX 计数 |
| 每核 CPU | mpstat -P ALL 1 10 | 系统、软中断、idle |
| 每线程 | pidstat -t -p "$PID" 1 10 | 线程热点和调度 |
| socket | ss -tinm；ss -u -a -m | 队列、内存、TCP 状态 |
| 协议统计 | nstat -az | 同窗口差分 |
| 出口队列 | tc -s qdisc show dev "$IFACE" | backlog、drops |
| NUMA | numactl --hardware；numastat -p "$PID" | 拓扑与进程分配 |

## 使用方式

在实验前后保存相同命令的输出并记下时间，用增量解释问题。计数器累计值来自开机以来或设备创建以来，通常不是当前速率。

字段应查本机 man、内核与驱动文档。/proc/net/softnet_stat 的列随版本演进，不在本仓库固定死列号；需要解码时匹配运行内核源码。

自动化采集见 [scripts](../scripts/README.md)，默认只采环境和计数，不抓业务载荷。

参考：[接口统计](https://docs.kernel.org/networking/statistics.html)、[Linux Scaling](https://docs.kernel.org/networking/scaling.html)。
