# Linux 收发包路径与观测点

范围：常见 Linux 主机网络路径的简化模型。XDP、硬件卸载、虚拟设备和驱动差异可能绕开部分节点。

## 收包路径

网卡分类与 RX 队列 → DMA/描述符 → 中断或轮询触发 → NAPI → 协议栈处理 → socket 队列 → 应用读取。转发流量通常进入路由/过滤/出口路径，不必进入本机应用 socket。

## 发包路径

应用写入 → socket/传输层 → 路由与过滤 → qdisc/设备发送队列 → 驱动 TX 描述符 → 网卡发出。TX completion 代表可以回收资源的时机，不等于远端应用已收到。

| 位置 | 观察方式 | 要判断的问题 |
| --- | --- | --- |
| 物理端口 | ethtool 链路与统计 | 链路是否降速、错误是否增长 |
| RX/TX 队列 | 驱动 per-queue 计数 | 是否负载集中、描述符压力 |
| CPU/中断 | /proc/interrupts、mpstat | 哪些核在处理收发 |
| NAPI/软中断 | /proc/softirqs、perf | 接收工作是否占据 CPU |
| 协议层 | nstat、ss | 重传、监听溢出、socket 压力 |
| 应用层 | pidstat、调用栈、业务指标 | 处理或读取是否跟得上 |
| 出口排队 | tc -s qdisc | 排队、丢弃与整形是否符合预期 |

计数器应做相同时间窗口的差分。多个层次可能重复统计同一异常，不能把所有 dropped 简单相加。

## NAPI 的关键边界

NAPI 通常由中断调度 poll，一次 RX 处理有 budget。持续有工作时可能继续轮询；也存在忙轮询和线程化模式。因此“每个包一次中断”和“NAPI 永远不用中断”都不准确。

如果软中断忙，先定位哪类工作、哪个队列和哪个核，再评估分流、应用读取速度或包处理逻辑。预算调大可能只是让接收处理占用 CPU 更久。

## 现场操作

先运行[只读命令速查](../observability/commands.md)，再按照[丢包排查](../troubleshooting/packet-loss.md)逐层缩小范围。使用抓包验证时记录抓取位置与 offload 状态，避免把主机内的大包表示当成线上大帧。

参考：[NAPI](https://docs.kernel.org/networking/napi.html)、[接口统计](https://docs.kernel.org/networking/statistics.html)。
