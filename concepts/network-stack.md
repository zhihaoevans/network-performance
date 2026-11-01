# 网络与 Linux 术语

[返回概念索引](README.md)

## 协议与传输

| 术语 | 英文 | 定义与性能意义 |
| --- | --- | --- |
| MTU | Maximum Transmission Unit | 接口可承载的最大网络层包大小；不是应用有效载荷，也不是完整以太网帧长度。 |
| MSS | Maximum Segment Size | TCP 段的数据部分大小上限，不含 IP/TCP 头。实际发送还受路径与选项等约束。 |
| 路径 MTU | Path MTU / PMTU | 路径上可用 MTU 的限制；封装可能减少可供内层使用的空间。 |
| BDP | Bandwidth-Delay Product | 带宽与延迟的乘积；讨论 TCP 在途数据通常使用 RTT，结果要统一为 bit 或 byte。 |
| 拥塞窗口 | Congestion Window / cwnd | 发送端拥塞控制对在途数据的限制。 |
| 接收窗口 | Receive Window / rwnd | 接收端通告的接收能力，用于流量控制。 |
| 流量控制 | Flow Control | 防止发送速度超过接收端承受能力。 |
| 拥塞控制 | Congestion Control | 根据网络反馈调整发送行为，避免或缓解网络拥塞。 |
| 队头阻塞 | Head-of-Line Blocking / HOL | 前序工作未完成，阻碍后续工作继续推进；要区分队列、传输与应用层。 |
| 缓冲膨胀 | Bufferbloat | 持续积压在过大的缓冲队列中导致延迟显著增大。 |

TCP 基本定义参考 [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html)，BDP 与测试口径参考 [RFC 6349](https://www.rfc-editor.org/rfc/rfc6349.html)。

## 收发路径与分流

| 术语 | 英文 | 定义与性能意义 |
| --- | --- | --- |
| RX / TX | Receive / Transmit | 接收 / 发送；必须注明是哪个端口或主机视角。 |
| IRQ | Interrupt Request | 设备通知 CPU 的中断；中断亲和性影响处理位置。 |
| softirq | Software Interrupt | 内核延后处理工作的一种机制；网络收发常涉及软中断上下文。 |
| NAPI | NAPI | Linux 网络事件处理机制，常由中断触发后进行轮询；也支持忙轮询或线程化处理等方式。 |
| budget | Poll Budget | 一轮 NAPI poll 可处理的接收工作量限制，不等于整个系统的固定包数上限。 |
| RSS | Receive Side Scaling | 网卡把流量分配到 RX 队列，通常使用报文头哈希和间接表。 |
| RPS | Receive Packet Steering | 软件选择处理接收协议栈的 CPU。 |
| RFS | Receive Flow Steering | 考虑消费流量的应用位置，改善接收处理的 CPU 局部性。 |
| XPS | Transmit Packet Steering | 按 CPU 或接收队列映射等信息选择发送队列。 |
| qdisc | Queueing Discipline | Linux 出口排队与调度机制，可承载整形等策略。 |
| skb | sk_buff | Linux 网络栈的重要包描述结构；数据不一定全部连续存放。 |

RSS 不能保证把单条流均匀拆到所有核；RPS 也不是无成本增加性能。分流与局部性参考 [Linux scaling](https://docs.kernel.org/networking/scaling.html)，事件处理参考 [NAPI 文档](https://docs.kernel.org/networking/napi.html)。

## 分段、聚合与卸载

| 术语 | 英文 | 定义与注意事项 |
| --- | --- | --- |
| TSO | TCP Segmentation Offload | 把 TCP 大块数据的分段工作交给支持的网卡。 |
| GSO | Generic Segmentation Offload | 内核通用分段机制，允许较大包表示在栈中流转并在需要时分段。 |
| GRO | Generic Receive Offload | 接收侧聚合符合条件的包，减少后续逐包处理成本。 |
| 校验和卸载 | Checksum Offload | 由硬件承担部分校验和计算或验证。 |

分段与 IP 分片不是同一个过程。主机抓包位置可能位于分段前、聚合后或硬件计算校验和之前，因此看到的大包或校验和提示不必然是线上异常。参考 [Linux Segmentation Offloads](https://docs.kernel.org/networking/segmentation-offloads.html)。
