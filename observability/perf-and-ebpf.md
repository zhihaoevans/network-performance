# perf 与 eBPF：把瓶颈定位到路径

## 先提出问题，再选择工具

| 问题 | 方法 | 局限 |
| --- | --- | --- |
| CPU 时间花在哪里 | perf 采样调用栈 | 不能直接解释睡眠等待 |
| 每包指令/周期变化 | perf stat 与包计数差分 | PMU、复用和频率影响解释 |
| 线程为什么没运行 | 调度/等待事件追踪 | 需要关联 PID、时间与负载 |
| 哪个阶段发生丢弃 | 可用 tracepoint 或 BPF | 内核版本、符号与功能支持 |
| 业务 P99 为什么异常 | 应用埋点 + 系统事件关联 | 各层时间基准要一致 |

## 有界采样示例

```bash
PID=1234  # 替换为目标进程
perf stat -p "$PID" -e cycles,instructions,cache-misses -- sleep 10
perf record -F 99 -g -p "$PID" -- sleep 10
perf report --stdio
```

record 会在当前目录生成 perf.data，包含进程与符号信息；采集应在受控输出目录。PMU 不可用或权限不足时记录失败，不能把缺失计数当零。调用栈质量与编译选项、符号和展开机制有关。

## 阅读结果

CPU 采样图中的宽度代表样本占比，不是函数单次耗时。等待很久但不消耗 CPU 的路径可能不突出。进程采样未必覆盖 IRQ/其他线程工作，必要时在受控测试机使用系统范围采样。

IPC、cache miss 和 branch miss 都是线索。比较前保证事件定义和采样范围一致；cache-misses 并不自动等于跨 NUMA 内存访问次数。

## eBPF 的使用边界

先枚举当前内核可用事件与工具版本，再选择稳定 tracepoint。kprobe 依赖符号和实现细节；BTF/CO-RE 解决部分类型适配，不保证任何脚本跨所有内核适用。

把输出聚合成计数/直方图，控制键数量与采样量；逐事件打印可能显著扰动结果。记录开启和关闭观测时基线差异。

参考：[perf 权限与数据](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html)、[BPF 文档](https://docs.kernel.org/bpf/index.html)。
