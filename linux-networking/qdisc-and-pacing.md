# 出口队列、整形与发送节奏

## 区分三个目标

- 调度：多个包或流之间按什么顺序服务。
- 整形：把发送速率约束在目标范围，可能引入排队。
- pacing：让发送更均匀，减少一次性突发。

仅提高队列容量可能减少短时丢弃，但增加等待。持续 offered load 高于服务能力时，任何有限队列最终都会满。

## 观察

```bash
IFACE=eth0
tc -s qdisc show dev "$IFACE"
tc -s class show dev "$IFACE"
ip -s link show dev "$IFACE"
```

记录 backlog、drops、overlimits 与测量窗口。overlimits 可能是整形行为统计，不可直接等同丢包。接口存在多队列时要理解 root 与子 qdisc 的层级。

## 实验方法

先定义目标：控制出口速率、降低突发，还是压低负载下的 RTT。以相同业务负载比较默认配置与候选方案，同时看吞吐、丢弃、排队、CPU 和低速流体验。

netem 用于可控实验的延迟/丢包/重排注入，不是通用生产调优器。它改变的是指定接口的出口路径；双向 RTT 的变化必须结合放置位置解释。

## 配置与恢复

root qdisc 的替换会影响整个出口调度。只在实验接口操作，提前保存配置结构与创建命令；tc 的统计输出不是完整可执行备份。若只是在全新 veth 上添加 netem，删除该 qdisc 或删除实验拓扑可以恢复；不要把这种恢复办法用于已有业务配置。

参考：[tc-netem(8)](https://man7.org/linux/man-pages/man8/tc-netem.8.html)。可复现步骤：[namespace/netem 实验](../labs/002-netns-netem.md)。
