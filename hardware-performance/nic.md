# 网卡：速率、PPS 与测量边界

状态：规格参考与理论演算，非转发实测。核对日期：2026-11-03。

## 标准帧开销下的 PPS 上限

以全双工 Ethernet 的单方向 MAC 速率计算：帧长 L 包含 MAC 头和 4 B FCS，不含前导码/SFD；额外计入 8 B 前导码/SFD 和平均 12 B 时间的帧间隙。

`PPS = 速率(bit/s) / ((L + 20) × 8)`

| MAC 速率 | 64 B 帧 | 1518 B 帧（无 VLAN、1500 B payload） |
| --- | --- | --- |
| 1 Gb/s | 1.488 Mpps | 0.081 Mpps |
| 10 Gb/s | 14.881 Mpps | 0.813 Mpps |
| 25 Gb/s | 37.202 Mpps | 2.032 Mpps |
| 40 Gb/s | 59.524 Mpps | 3.251 Mpps |
| 100 Gb/s | 148.810 Mpps | 8.127 Mpps |
| 200 Gb/s | 297.619 Mpps | 16.255 Mpps |

均为公式结果，保留三位小数。假设连续发送、无额外封装/暂停；不重复扣除 PHY 编码/FEC，也不将 FEC 的物理比特率当作 MAC 速率。来源：[NetApp 对 Ethernet 帧、前导码与 IFG 的计算说明](https://kb.netapp.com/on-prem/ontap/Perf/Perf-KBs/What_is_the_theoretical_maximum_throughput_of_a_Gigabit_Ethernet_interface)。

1518 B 帧的 1500 B 是 L2 payload，并非 TCP/UDP 应用数据。VLAN、隧道、TCP 选项需按实际帧长重算。抓包和 DPDK 常不包含 FCS，所谓“64 字节包”必须确认计数口径。IFG 是空闲时间，不是帧里的 12 B 数据。

## 有型号范围的规格样例

[NVIDIA ConnectX-6 Dx 数据表（OCT21）](https://www.nvidia.com/content/dam/en-zz/Solutions/networking/ethernet-adapters/ConnectX-6-Dx-Datasheet.pdf)公布：

| 指标 | 厂商公布值 | 引用边界 |
| --- | --- | --- |
| 产品最大总网络带宽 | 200 Gb/s | 不是每个端口都可各跑 200G |
| 网络端口数 | 1 / 2 | 对应不同型号 |
| 主机接口 | PCIe Gen4 x16 | 实际卡型号和协商状态需另查 |
| DPDK message rate | 最高 215 Mpps | 数据表未给出完整测试条件，不能当保证值或目标机实测 |

[官方接口手册](https://networking-docs.nvidia.com/connectx6dxhw/interfaces)说明该系列支持双口 10/25/40/50/100Gb/s 或单口 200Gb/s，卡型可为 x8/x16。必须保留 OPN、固件、驱动、DPDK/PMD、PCIe 实际速率与端口配置。厂商消息率不能替代双口收发/转发的实测。

## 实际观测

替换接口名，以下命令只读：

```bash
ethtool eth0
ethtool -i eth0
ethtool -l eth0
ethtool -g eth0
ethtool -c eth0
ethtool -k eth0
ethtool -S eth0
```

区分最大/当前队列数、ring 大小、驱动计数器和硬件实际丢包。DPDK 接管接口后通常需通过 PMD/testpmd 查询。延迟还受中断合并、轮询、批量、PCIe/NUMA 与排队影响；记录测量起止点、包长、负载、时钟同步、P50/P99 和丢包。未测量前不提供固定“网卡延迟”。

相关：[PCIe 预算](pcie.md) · [网卡调优](../nic-and-hardware/nic-tuning.md)。
