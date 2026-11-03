# 核间互连与 Cache-to-cache

状态：配置参考与测量方法；跨核时延待测。核对日期：2026-11-03。

## 有配置范围的互连数据

[NASA HECC Aitken Cascade Lake 配置](https://www.nas.nasa.gov/hecc/support/kb/cascade-lake-processors_579.html)中的 Xeon Gold 6248 节点为双 socket，采用片上 mesh；每对 socket 实装两条 UPI 链路，每条传输率 10.4 GT/s。处理器支持最多三条链路，不能把处理器支持数当作主板实装数。

GT/s 不是应用 GB/s；一致性请求、响应与数据流量共享互连资源。这里只引用链路数量与传输率，不用线路速率推断应用带宽。该配置也不能外推到后续 UPI 或 AMD Infinity Fabric。

| 指标 | 数值状态 | 关键条件 |
| --- | --- | --- |
| 同 socket 不同核 cache-to-cache 时延 | 待测 | 核位置、缓存域、cache line 状态 |
| 跨 socket cache-to-cache 时延 | 待测 | socket/node、链路、snoop、并发 |
| 原子变量 ping-pong 往返耗时 | 待测 | 内存序、同步协议、线程绑定 |
| 持续跨 socket 有效数据带宽 | 待测 | 读写方向、NUMA 放置、工作集 |

原子 ping-pong 的往返包含两端同步与循环开销，不能直接命名为“单次 cache line 传输延迟”。跨核访问、远端 DRAM 与本地 LLC hit 也不是同一指标。

## 定位共享与争用

对实际测试程序可运行：

```bash
perf c2c record -- ./your-workload
perf c2c report --stdio
```

需替换程序名，命令会执行程序并写入采样文件；硬件、内核与权限必须支持相应内存事件。记录采样配置与程序开销，HITM 样本反映一致性相关现象，不能将样本数量直接等同为全部传输次数或固定 ns。

来源：[Linux perf c2c 文档](https://kernel.googlesource.com/pub/scm/linux/kernel/git/next/linux-next/+/master/tools/perf/Documentation/perf-c2c.txt)。在线文档需对应运行版本。[Intel MLC](https://www.intel.com/content/www/us/en/developer/articles/tool/intelr-memory-latency-checker.html)也提供 `--c2c_latency`；副作用与记录要求见[测量方法](measurement.md)。

比较每核独立计数器、共享计数器和 padding 前后效果时，保持工作量、线程绑定与负载一致，同时记录内存占用。HITM 热点可能是必要的真实共享；需结合源码判断 false sharing。
