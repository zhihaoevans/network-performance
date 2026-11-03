# TLB 与地址翻译

状态：架构资料参考与覆盖范围演算，非页表遍历时延实测。核对日期：2026-11-03。

## Skylake / Cascade Lake 样例

依据 Intel Optimization Reference Manual 248966-049US，附录 C 表 C-1 的 Skylake / Cascade Lake 列：

| 结构 | 页大小 | 项数 | 相联度 |
| --- | --- | --- | --- |
| L1 ITLB | 4 KiB | 128 | 8-way |
| L1 ITLB | 2 MiB / 4 MiB | 每线程 8 | 参见手册线程划分说明 |
| L1 DTLB | 4 KiB | 64 | 4-way |
| L1 DTLB | 2 MiB / 4 MiB | 32 | 4-way |
| L1 DTLB | 1 GiB | 4 | 4-way |
| 统一 STLB（指令/数据） | 4 KiB 与 2 MiB 共享 | 1536 | 12-way |
| 统一 STLB | 1 GiB | 16 | 4-way |

来源：[Intel 248966-049US，附录 C](https://cdrdv2-public.intel.com/814198/248966-Optimization-Reference-Manual-V1-049.pdf)。上述为该表中的结构容量；SMT 下的划分规则会影响单逻辑 CPU 可用项数，不能将整核容量直接视为每个线程独享。

按全部条目用于同一种页大小演算：64 × 4 KiB = 256 KiB；1536 × 4 KiB = 6 MiB；1536 × 2 MiB = 3 GiB。它们是理想地址覆盖范围，不是 cache 容量或性能保证。STLB 的 4 KiB/2 MiB 项共享，不能把两种覆盖范围同时相加；冲突、SMT 划分与混合页使用会降低有效覆盖。

L1 TLB miss 可能命中 STLB；STLB miss 后页表遍历仍可能命中 CPU cache。不能将一次 TLB miss 固定折算成某个 DRAM 时延。虚拟机还需考虑嵌套地址转换。

## 与网络程序的关系及观察

大规模连接表、随机规则查找和 mbuf pool 可能增加翻译压力。Hugepage 可作为减少页数的候选措施，但会改变分配、NUMA 放置和内存占用，收益需要同负载比较。

先执行 `perf list`，选择对应 CPU 支持的 DTLB/ITLB walk 与 miss 事件；保留具体事件定义、运行比例与归一化分母。不能拿通用 miss 事件名称保证它覆盖所有翻译层级。记录实际页大小、THP/hugetlb 状态、SMT 与 NUMA 页归属；具体实验记录见[测量方法](measurement.md)。
