# LAB-001：TCP/UDP 双端基线

状态：可执行实验步骤；本仓库尚无该实验的实测性能结果。

## 环境

两台可控制的 Linux 主机，安装 iperf3。只在双方允许的实验链路发送测试流量。记录两端版本、接口、链路速率、CPU/NUMA、MTU、offload 和中间设备。SERVER 替换为服务端实验地址。

## 服务端

```bash
iperf3 --version
iperf3 -s
```

默认使用 5201 端口；TCP 控制连接要能到达，UDP 实验还需相应 UDP 数据路径。

## 客户端

在新的结果目录执行：

```bash
SERVER=198.18.0.2  # 替换为实际实验地址
mkdir -p results
iperf3 -c "$SERVER" -t 20 -O 3 -P 1 -J > results/tcp-forward-1.json
iperf3 -c "$SERVER" -t 20 -O 3 -P 1 -R -J > results/tcp-reverse-1.json
iperf3 -c "$SERVER" -t 20 -O 3 -P 4 -J > results/tcp-parallel-1.json
iperf3 -c "$SERVER" -u -b 10M -l 1200 -t 20 -J > results/udp-10m-1.json
```

10M 是保守起步示例，不代表适合所有链路。-l 是 UDP 应用数据长度，不是以太网帧长。每组独立重复至少三次，改文件编号避免覆盖；不要把所有组并发执行。

同步采集两端 CPU 和计数器。工具的 UDP jitter 不等于业务延迟 P99。

## 结果

运行 [summarize_iperf.py](../scripts/README.md) 汇总 TCP 接收吞吐、UDP 接收吞吐/丢包和 jitter；原始 JSON 仍需保留。脚本不代替对发送端能力与测量口径的检查。

填写[实验报告](../templates/experiment.md)，解释方向差异、多流收益和波动；所有未测量项写 N/A。

## 停止与恢复

客户端结束后服务端 Ctrl-C。本文不修改 sysctl/网卡配置，无需系统参数回滚；移除临时开放的测试访问规则（如果曾手动添加）。

参考：[iperf3](https://software.es.net/iperf/invoking.html)。命令是否可用以安装版本 help/man 为准。
