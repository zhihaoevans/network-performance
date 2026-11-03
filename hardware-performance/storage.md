# SSD / NVMe 性能数据

状态：厂商规格样例与计算方法，非仓库实测。核对日期：2026-11-03。

## 型号和测试条件一起引用

以下仅摘录 Samsung 990 PRO 2 TB（MZ-V9P2T0）在 2022 年 Rev.1.0 数据表中的最高值，接口为 PCIe Gen4 x4 / NVMe 2.0：

| 项目 | 厂商最高值 | 条件 |
| --- | --- | --- |
| 顺序读 | 7450 MB/s | 厂商测试环境 |
| 顺序写 | 6900 MB/s | Intelligent TurboWrite 启用 |
| 随机读 | 22K IOPS | QD1、1 线程 |
| 随机读 | 1400K IOPS | QD32、16 线程 |

MB/s 为十进制，K = 1000。来源：[Samsung 990 PRO 数据表 Rev.1.0，第 3–4 页](https://download.semiconductor.samsung.com/resources/data-sheet/Samsung_NVMe_SSD_990_PRO_Datasheet_Rev.1.0_10129514051890.pdf)。

测试使用 IOmeter 1.1.0、Ryzen 7 5800X、32 GB DDR4、ASRock X570 Taichi、Windows 10 Pro 64bit，SSD 作为第二块盘。上述数据表未完整列明这些测试的块大小、顺序测试队列设置和预处理过程；不能自行补写为“4 KiB 稳态实测”。QD32/16 线程也不能简写成全盘仅 32 个在途请求。

写入值依赖 TurboWrite 的适用传输量，不保证缓存耗尽后的持续写速率。不要将 2 TB 结果复制到 1 TB 或其他容量；固件、温度、剩余容量和预处理均影响性能。

## IOPS、带宽与时延

同一块大小下：带宽(B/s) = IOPS × 每次 I/O 字节数。例如假设 100K IOPS、4 KiB I/O，得到 409.6 MB/s；这是演算，不是某个 SSD 的实测。

稳态且统计边界一致时，平均在途请求数 = 完成率 × 平均响应时间（Little 定律）。因此高队列并发下的 1/IOPS 是平均完成间隔，不能当作单请求平均延迟或 P99。厂商“最高 IOPS”也不能推算低负载时延。

## 目标机器需要补充的结果

分别测量 QD1 与高并发、顺序与随机、读写与混合负载，记录块大小、每线程深度、线程数、I/O 引擎、direct/buffered、文件系统、测试范围、预热、稳态、固件、温度、填充率、运行时间和重复次数。给出 IOPS、带宽、平均/P99/P99.9 时延与错误，不把 fio 的 slat/clat/lat 混用。

写测试必须使用专用可丢弃测试文件或测试盘，并明确覆盖范围；本次只整理资料，未执行设备读写基准。将测试原始输出与[实验模板](../templates/experiment.md)关联。抓包落盘场景还需比较持续写入与上游流量，计算缓存能覆盖的突发时长。
