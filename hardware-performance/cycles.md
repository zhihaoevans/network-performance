# CPU 周期与时间换算

状态：公式推导与参考说明。核对日期：2026-11-03。

## 机器周期的口径

本文使用 CPU 时钟周期（cycle）。旧教材中的“机器周期”可能指完成某种基本操作所需的多个时钟周期，不能直接套到现代乱序 CPU。一条指令的时延、倒数吞吐率和 CPI 也是不同指标；数据依赖、并行执行与 cache miss 都会改变程序的 CPI。

在频率恒定且计数属于同一个时钟域时：

- 单周期时间：T(ns) = 1 / f(GHz)。
- N 个周期耗时：t(ns) = N / f(GHz)。
- IPC = retired instructions / CPU cycles；CPI 为对应计数口径下的倒数。
- cycles/packet = 被测 CPU 周期数 / 同一范围内处理包数。

| 假设恒定频率 | 单周期时间 | 100 cycles |
| --- | --- | --- |
| 1 GHz | 1 ns | 100 ns |
| 2 GHz | 0.5 ns | 50 ns |
| 2.5 GHz | 0.4 ns | 40 ns |
| 3 GHz | 约 0.3333 ns | 约 33.33 ns |
| 4 GHz | 0.25 ns | 25 ns |

以上均为数学换算，频率是示例输入。睿频、降频、空闲状态和迁核会使固定频率换算失效。多核周期数求和后除以频率得到的是聚合 CPU 时间口径，不能直接当作请求的墙钟延迟。

## Linux 观测

先用 `perf list` 确认事件支持，再针对实际程序采集：

```bash
perf stat -e cycles,instructions,ref-cycles -- ./your-workload
```

需替换程序名。PMU 权限、虚拟化、混合核和事件复用会影响结果；保留事件的运行比例和不支持提示。不能把 TSC tick、reference cycles 与实际核心 cycles 当成同一计数器，也不能用标称频率直接换算任意时间戳。跨核/跨机时间戳需先确认同步与时钟语义。

来源：[Linux perf stat 文档](https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-stat.txt)（在线 master，使用时对应本机内核/perf 版本）；具体 PMU/TSC 语义查 [Intel 架构手册入口](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)。
