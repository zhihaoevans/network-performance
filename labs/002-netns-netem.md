# LAB-002：namespace/veth 与可控延迟

状态：实验步骤，未在真实链路实测。要求 Linux、root 或相应网络管理能力、iproute2、ping、iperf3、netem 支持。此实验不经过物理网卡，不能验证硬件线速。

## 创建隔离拓扑

先检查名字未使用；若存在，停止并换名字，不删除未知对象：

```bash
ip netns list
ip link show
```

确认 np-a、np-b、np-va、np-vb 均未被占用后：

```bash
sudo ip netns add np-a
sudo ip netns add np-b
sudo ip link add np-va type veth peer name np-vb
sudo ip link set np-va netns np-a
sudo ip link set np-vb netns np-b
sudo ip -n np-a addr add 198.18.0.1/30 dev np-va
sudo ip -n np-b addr add 198.18.0.2/30 dev np-vb
sudo ip -n np-a link set lo up
sudo ip -n np-b link set lo up
sudo ip -n np-a link set np-va up
sudo ip -n np-b link set np-vb up
sudo ip netns exec np-a ping -c 5 198.18.0.2
```

## 基线与干预

终端一启动服务端：

```bash
sudo ip netns exec np-b iperf3 -s
```

终端二测基线后，在 np-b 出口加延迟：

```bash
sudo ip netns exec np-a iperf3 -c 198.18.0.2 -t 10
sudo ip netns exec np-b tc qdisc add dev np-vb root netem delay 10ms
sudo ip netns exec np-a ping -c 10 198.18.0.2
sudo ip netns exec np-a iperf3 -c 198.18.0.2 -t 10
sudo ip netns exec np-b tc -s qdisc show dev np-vb
```

10ms 加在单方向出口，对 ping 的 RTT 预计贡献约 10ms，而不是自动增加 20ms；调度与排队会带来偏差。TCP 吞吐变化还受窗口、ACK、CPU 和工具影响。netem 放置与 TCP small queues 交互会影响逼真度，真实 WAN 测试应使用独立中间节点并验证实际时延/丢包。

## 恢复与清理

先删除实验添加的 qdisc 并复测，再在终端一 Ctrl-C 停止服务端：

```bash
sudo ip netns exec np-b tc qdisc del dev np-vb root
sudo ip netns exec np-a ping -c 5 198.18.0.2
sudo ip netns pids np-a
sudo ip netns pids np-b
```

确保没有实验进程仍在运行后，只删除本次创建的 namespace：

```bash
sudo ip netns del np-a
sudo ip netns del np-b
```

创建中途失败时按实际成功步骤清理；若 veth 尚未移入 namespace，则检查并删除本次创建的 np-va。不要自动清理同名但来源不明的资源。

验收：基线、干预、恢复三组 RTT，记录实际 qdisc、吞吐和环境。参考：[tc-netem](https://man7.org/linux/man-pages/man8/tc-netem.8.html)。
