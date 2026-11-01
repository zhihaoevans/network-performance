# 容器、虚拟机与云网络

## 先画实际路径

同节点 Pod、跨节点 Pod、Service、外部入口、NAT 与 host network 路径可能不同。记录 veth、bridge、路由、overlay、负载均衡与过滤链；不要只按“容器网络”归类。

| 变量 | 对比方法 | 必须保持一致 |
| --- | --- | --- |
| 同节点/跨节点 | 分别测量 | 实例规格、应用与负载 |
| 直连/Service | 逐段增加路径 | 后端数量与会话行为 |
| overlay/直接路由 | 明确 CNI 实现 | MTU、策略与底层链路 |
| 容器/host network | 控制进程资源 | CPU 配额、亲和性与安全策略 |
| VM/SR-IOV | 分开建立基线 | 队列、NUMA、设备能力 |

这些对比是诊断设计，不代表某种模式必然更快。

## CPU 配额与尾延迟

在 cgroup v2 查看被测进程实际 cgroup 的 cpu.max、cpu.stat 和 cpuset.cpus.effective。检查 nr_throttled/throttled_usec 的增量是否与慢窗口相关。宿主机空闲不代表容器没有被节流。

## Conntrack

检查是否经过状态跟踪、当前 count/max、失败统计与连接生命周期。容量问题与查找/创建开销不同；扩表不能自动解决每秒建连压力，也会增加内存需求。

## MTU 与封装

外层封装消耗额外空间，内层 MTU 需匹配实际路径。以小包通、大包失败为线索时检查 PMTU 和 ICMP 反馈，不默认禁用 PMTU。

## 云环境补充

记录实例网络限额、PPS/带宽/连接限制、突发额度与宿主共享因素；这些信息随供应商和规格变化，应引用当前实例官方资料。虚拟机的 perf/硬件计数不可用时，明确观测盲区。

参考：[cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)、[conntrack](https://www.kernel.org/doc/html/latest/networking/nf_conntrack-sysctl.html)。
