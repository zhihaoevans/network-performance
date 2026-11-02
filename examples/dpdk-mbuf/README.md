# 第一个 DPDK 程序：mbuf 生命周期

示例只做 EAL 初始化、内存池创建、mbuf 分配/追加数据/释放和资源检查，不收发真实网络数据。

在 Codespace 仓库根目录：

```bash
make -C examples/dpdk-mbuf
python3 scripts/dpdk_lab.py mbuf
```

预期输出包含 `payload=hello DPDK`、相同的 pool before/after 以及 `PASS: mbuf returned to pool`。字符串长度包含结尾 NUL，不能将它当作协议报文。

可练习：修改 payload；观察 headroom/tailroom；批量分配并检查错误分支；给 pool 留出不足对象，验证失败处理。每次保证所有分配对象归还后再释放 pool。

调试时先执行 `python3 scripts/dpdk_lab.py mbuf --dry-run`，将输出数组中的程序和参数传给 `gdb --args`。CPU 映射由可用 affinity 决定，不固定假设 CPU 0 可用。

配置说明：[Codespaces](../../dpdk/codespaces.md)。
