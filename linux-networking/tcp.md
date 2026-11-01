# TCP 吞吐量、窗口与连接性能

## 先判断限制来自哪里

| 现象 | 候选限制 | 验证点 |
| --- | --- | --- |
| 长 RTT 下单连接吞吐低 | 在途数据不足、拥塞或丢包 | ss 中 RTT、cwnd、重传及接收窗口信息 |
| 大量重传 | 路径丢包、乱序、接收压力 | 两端抓包与网卡/协议计数 |
| 多连接显著更快 | 单流处理或窗口限制 | 每核、每队列、单连接状态 |
| 小请求响应慢 | 应用凑包、调度、Nagle/ACK 交互 | 应用时间戳与报文时序 |
| 新连接失败 | 监听队列、FD、端口或状态表 | 错误码、监听统计、conntrack |

## 窗口和缓冲区不是一个东西

cwnd 是拥塞控制约束，rwnd 是接收端通告能力，socket 缓冲区承载端系统数据。有效吞吐受这些因素以及发送节奏、RTT、丢包和应用速率共同影响。

粗略判断可使用 BDP = 目标 bit/s × RTT / 8；它只是所需在途字节的量级参考，不是必须设置的 sysctl 值。

## 观察命令

在两端记录相同窗口：

```bash
ss -tinm
nstat -az
sysctl net.ipv4.tcp_congestion_control
sysctl net.ipv4.tcp_available_congestion_control
sysctl net.ipv4.tcp_rmem net.ipv4.tcp_wmem
sysctl net.core.rmem_max net.core.wmem_max
```

ss 输出字段会随版本变化。nstat -az 输出绝对统计，适合自行做差；不要把历史累计重传数解释为本次重传率。

## 调优决策

- 应用读取慢：先优化消费路径；堆积更多数据只是延后问题。
- 证据指向窗口不足：检查自动调节、应用是否显式设置缓冲以及内存预算，再对单连接实验。
- 小消息交互：在应用层比较有界批处理与 TCP_NODELAY；后者可能增加包数和 CPU。
- 连接成本高：比较连接复用，同时记录连接生命周期和故障恢复语义。
- 拥塞控制：只比较本机可用算法，固定 RTT、损失、负载和队列条件；没有通用最优算法。

不提供“全局调优参数包”。变更应先在可控环境进行，保存原值，用新连接复验，再恢复。

## 常见误判

TIME_WAIT 是 TCP 生命周期的一部分，数量高不能单独证明故障。不要直接归因为需要缩短所有超时。发送端 write 成功也不意味着接收端应用完成处理。

参考：[tcp(7)](https://man7.org/linux/man-pages/man7/tcp.7.html)、[IP sysctl](https://docs.kernel.org/networking/ip-sysctl.html)。实践：[TCP/UDP 基线](../labs/001-network-baseline.md)。
