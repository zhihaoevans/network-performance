# DPDK 基线：先量清 testpmd

## 前提

使用独立实验端口、匹配版本的 DPDK、驱动和固件。记录 CPU/NUMA、hugepages、IOMMU、设备绑定方式与流量发生器。设备绑定可能让 Linux 失去该网口，不能盲目解绑管理网口；部分 PMD 使用不同设备模型。

testpmd 是基础转发测试工具，结果不代表加入 ACL、连接跟踪、DPI、加密或 AI 检测后的业务性能。

## 命令结构示意

以下 BDF 和 CPU 都是示例，必须替换并核对本机版本支持：

```bash
sudo dpdk-testpmd -l 2-4 -n 4   -a 0000:01:00.0 -a 0000:01:00.1 --   -i --nb-cores=2 --rxq=2 --txq=2 --forward-mode=io
```

双横线前是 EAL 选项，后面是应用选项。-n 是内存通道参数，不是 RX 队列数量；需按平台确认，不把示例数值当推荐值。CPU 列表中需为主线程和转发线程留出资源。

交互命令：

```text
show port info all
show config fwd
show port stats all
show port xstats all
start
stop
show port stats all
quit
```

开始前核对端口映射、链路、转发流分配以及源/目的 MAC 的处理方式。io 模式不替你完成业务路由。

## 基线矩阵

固定其他条件，依次改变帧长、流数、工作核数、队列数与 burst。每次记录发送器 offered load、接收器实际收到、端口计数、丢包、CPU 和延迟（若可测）。

测可接受丢包率下的速率时先定义阈值与窗口，再递增负载或二分搜索；每个候选点重复验证。不要只报告瞬时峰值。

## 结束与恢复

停止流量发生器，stop 转发，记录统计，再退出。若改变过设备驱动、hugepage 分配或 CPU 设置，应按事前记录恢复并检查 Linux 接口与连接。设备恢复命令依绑定模型而定，本文不提供一键解绑/重绑脚本。

参考：[启动选项](https://doc.dpdk.org/guides/testpmd_app_ug/run_app.html)、[运行命令](https://doc.dpdk.org/guides/testpmd_app_ug/testpmd_funcs.html)。实践：[LAB-005](../labs/005-dpdk-forwarding.md)。
