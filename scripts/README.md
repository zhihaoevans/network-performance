# 辅助脚本

依赖 Python 3.9+ 标准库，不需要 pip 安装。仓库根目录执行。脚本不自动调优、不修改 sysctl、不切换驱动、不发起性能流量。

## 只读环境采集

```bash
python3 scripts/collect_environment.py --interface eth0 --output /tmp/netperf-before
```

替换接口名。输出目录必须不存在，父目录必须存在；默认每个外部命令最多 5 秒。记录命令、时间、退出状态和原始输出，工具缺失/权限不足会被标记，不假装采集成功。脚本不会自动 sudo。

前后各采一次，使用不同目录。目录可能包含主机、接口、硬件与统计信息，提交前脱敏。采集不是原子快照，各命令的时间有先后；精确同步实验应另设计采集方式。

## iperf3 JSON 汇总

```bash
python3 scripts/summarize_iperf.py results/tcp-*.json
python3 scripts/summarize_iperf.py --format csv results/tcp-*.json > summary.csv
```

只支持完整的单向 TCP/UDP `iperf3 -J` JSON；支持 reverse 测试，但不支持 bidirectional、JSON stream 或不明确接收端身份的旧格式。

优先读取 end.sum_received；旧 UDP 仅在 end.sum.sender 明确为 false 时接受。缺失字段输出 null/CSV 空值，不将发送吞吐替代接收吞吐。输入失败时退出码 2 且不输出部分报告。

输出包含接收 Mbps、测量时长、TCP 发送重传、UDP 接收丢失/jitter 等。不会从 jitter 推导 P99，也不混合不同配置计算“平均性能”。重定向目标文件由 shell 创建，注意避免覆盖旧报告。

## 文档与工具检查

```bash
python3 scripts/check_docs.py
python3 -m unittest discover -s tests -v
```

文档检查覆盖本地内联 Markdown 链接目标与代码围栏，跳过代码块；不检查远端 URL、标题锚点、引用式链接或 Markdown 标题格式。工具测试使用合成数据，不能当作实测网络结果。

## 兼容范围

采集器允许 Linux 环境缺少 ethtool/numactl，并将缺项写入清单；结果解析器对不支持的 JSON 布局明确拒绝。真实 NIC/DPDK 和 iperf 性能实验需在目标机器验证。

本次验证：12 项工具测试通过；环境采集在受限 Linux 的 lo 接口冒烟运行，正确记录 11 项缺失/不可用项。测试环境没有 iperf3、ethtool 和真实 DPDK 网卡，因此未执行相关性能实验。
