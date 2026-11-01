# XDP、AF_XDP 与 DPDK 的选型边界

## 先按需求划分

| 路径 | 适合研究的问题 | 成本与限制 |
| --- | --- | --- |
| 内核 socket | 通用应用与成熟传输语义 | 协议栈、系统调用与调度 |
| XDP | 接收早期过滤/转发等有界处理 | 驱动模式、BPF 验证与功能约束 |
| AF_XDP | 用户态高性能包处理并利用 XDP 重定向 | UMEM/ring 管理、队列绑定和驱动能力 |
| DPDK | 专用数据平面与丰富 PMD/库 | 资源管理、驱动模型与运维集成 |

这是研究入口，不是跨机器性能排名。

## AF_XDP 的所有权

UMEM 为包数据提供存储，RX/TX ring 传递描述符，FILL 提供可接收缓冲，COMPLETION 归还可复用资源。处理前后必须明确哪个组件拥有 frame，避免提前复用或缓冲耗尽。

零拷贝与 copy 模式依设备/驱动和配置，不可仅凭使用 AF_XDP 就声称零拷贝。需记录实际绑定队列、运行模式与可用能力。

## 可比测试

对齐帧长、流数、CPU 数、NUMA、处理逻辑、校验与负载。过滤掉全部包和完整转发不是相同工作量；rxonly 与转发也不能直接比较。

观察 PPS、丢包、CPU、功耗（若可测）、部署复杂度和功能缺口。选型结论应解释为什么当前需求受益，而不是只贴峰值图。

参考：[AF_XDP](https://docs.kernel.org/networking/af_xdp.html)、[BPF](https://docs.kernel.org/bpf/index.html)、[DPDK Overview](https://doc.dpdk.org/guides/prog_guide/overview.html)。
