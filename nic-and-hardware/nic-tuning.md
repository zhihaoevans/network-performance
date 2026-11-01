# 网卡：链路、ring、合并与 offload

## 第一轮检查

```bash
IFACE=eth0
ethtool "$IFACE"
ethtool -i "$IFACE"
ethtool -g "$IFACE"
ethtool -l "$IFACE"
ethtool -c "$IFACE"
ethtool -k "$IFACE"
ethtool -S "$IFACE"
```

分别对应链路、驱动/固件、ring、通道、中断合并、卸载特性和统计。保存原始输出；不同驱动字段不能照字面直接类比。

## 调整方向与边界

| 机制 | 可验证假设 | 代价或限制 |
| --- | --- | --- |
| ring 增大 | 短时突发耗尽描述符 | 内存与排队增加，不改变持续处理上限 |
| 中断合并 | 小包中断成本较高 | 单包等待时间可能增加 |
| 多队列 | 流量可以分散到更多 CPU | 单流不一定获益，队列也有管理成本 |
| TSO/GSO/GRO | 摊薄逐包处理开销 | 改变抓包和软件包数口径 |
| Jumbo frame | 大数据传输减少逐包开销 | 全路径 MTU、一致性与业务兼容 |
| Pause/PFC | 特定网络的流量控制需求 | 可能传播拥塞，需端到端设计 |

不建议从“关闭所有 offload”开始。先保留正常配置测基线，再对证据相关特性做 A/B。

## 错误与丢弃

CRC/物理错误指向链路质量的可能性较高；missed/no-buffer 指标可能涉及队列服务或缓冲不足。具体语义必须查驱动实现与设备手册。接收应用慢与硬件丢弃可能同时存在，应追踪同一窗口。

## 恢复要求

每次修改都查询实际生效值。部分修改会导致接口短暂重启；用于 SSH 的管理接口不应当作实验对象。保存 ring、channel、coalesce 和 feature 原始值，不用“默认值”代替恢复值。

参考：[接口统计](https://docs.kernel.org/networking/statistics.html)、[分段卸载](https://docs.kernel.org/networking/segmentation-offloads.html)、[ixgbe 文档](https://docs.kernel.org/networking/device_drivers/ethernet/intel/ixgbe.html)。驱动文档只适用于相应设备。
