# 硬件性能数据参考

状态：参考说明；未在本仓库目标机器上实测。资料核对日期：2026-11-03。

本目录供 Linux 网络栈、DPDK 和高性能服务分析使用。每个数字必须连同架构、指标定义和条件一起引用。CPU/cache/TLB 数值样例以 Intel Skylake Server / Cascade Lake 为范围；另收录 PCIe Gen1–5 演算、ConnectX-6 Dx 与 Samsung 990 PRO 规格样例。其他型号需查各自资料并测量。

- [CPU 周期与时间换算](cycles.md)
- [Cache 容量、时延与数据口径](cache.md)
- [内存、NUMA 与带宽](memory.md)
- [PCIe 链路与带宽](pcie.md)
- [网卡速率与 PPS](nic.md)
- [TLB 与地址翻译](tlb.md)
- [核间互连与 Cache-to-cache](interconnect.md)
- [SSD / NVMe 性能数据](storage.md)
- [目标机器测量与记录](measurement.md)

## 引用规则

| 类型 | 如何使用 |
| --- | --- |
| 厂商公布的最小 load-to-use 时延 | 表示特定条件下的数据依赖访问下界，不能当平均值或 P99 |
| 集群维护方公布的配置与参考值 | 仅在对应型号与配置内引用；未提供原始测试时不能写成实测 |
| 公式推导 | 保留输入、单位与假设；不能写成硬件实测 |
| 目标机器实测 | 记录工具版本、命令、配置、原始输出与重复次数 |

L3、DRAM、本地/远端 NUMA、cache-to-cache 访问没有适用于所有机器的固定纳秒数。资料缺少足够条件时保留“待测”，不填入网络流传的经验常数。

相关内容：[NUMA 与布局](../nic-and-hardware/numa-and-memory.md) · [实验模板](../templates/experiment.md) · [返回首页](../README.md)
