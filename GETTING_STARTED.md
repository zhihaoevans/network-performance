# 从零开始使用参考库

## 不安装本地工具的开始方式

仓库已提供 [Codespaces DPDK 环境](dpdk/codespaces.md)，创建后自动编译 DPDK，并执行 EAL、mbuf 与 NULL PMD 功能自检。它用于学习与代码调试，真实 NIC 性能测试仍需独立硬件。

## 选择环境

| 环境 | 可以学习与验证 | 不能据此证明 |
| --- | --- | --- |
| Linux 单机 namespace | 路径、netem、协议现象 | 物理网卡线速、真实 NUMA I/O |
| 两台 Linux 主机 | TCP/UDP、链路与应用基线 | 所有生产业务负载 |
| 多队列 NIC + NUMA 主机 | IRQ、RSS、局部性 | 其他硬件同样收益 |
| DPDK 实验主机 + 发包器 | 转发、内存池、多核扩展 | 完整安全检测业务性能 |
| 容器/VM | 编排路径、资源限制 | 裸机硬件计数和物理拓扑 |

macOS 可以阅读、编辑和运行 Python 文档/结果处理工具；Linux sysctl、ethtool 和 namespace 实验需在 Linux 主机或 VM 内进行。

## 工具准备

按发行版包管理器安装：Python 3.9+、iproute2、ethtool、iperf3、sysstat、numactl、tcpdump；perf 选择与内核匹配的包。各发行版包名可能不同，以发行版仓库为准。不要求一开始安装 DPDK 或准备专用网卡。

先确认：

```bash
python3 --version
uname -r
ip -V
iperf3 --version
ethtool --version
```

缺少命令时先安装或记录环境限制；不要把“命令不可用”解释为“指标为零”。

## 第一次使用

1. 阅读[指标与术语](concepts/README.md)，明确目标指标。
2. 使用[方法论](fundamentals/methodology.md)写出测试目标。
3. 运行[环境采集](scripts/README.md)，记录原始状态。
4. 选择 [LAB-001](labs/001-network-baseline.md) 或 [LAB-002](labs/002-netns-netem.md)。
5. 使用[实验模板](templates/experiment.md)保存结果。
6. 按[症状入口](troubleshooting/README.md)定位下一项工作。

## 执行边界

命令分为只读检查、产生流量、改变配置。正文会说明后两类的前提与恢复。示例 IP/BDF/CPU/接口均需换成实验环境的实际值。管理连接与测试网口尽量分离；只对自己可控制、允许压测的链路发送负载。

## 最小可交付结果

完整环境记录 + 3 次基线 + 原始 JSON + 一条有数据支持的观察 + 下一条待验证假设。暂时没有硬件时完成 namespace 实验和读码笔记，并如实标记适用范围。
