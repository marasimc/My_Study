# 1. 查询CPU信息

```python
import psutil

# CPU逻辑数量
psutil.cpu_count()

# CPU物理核心
psutil.cpu_count(logical=False)

# 统计CPU的用户／系统／空闲时间
psutil.cpu_times()

# interval：每隔0.5s刷新一次
# percpu：查看所有的cpu使用率
for x in range(5):
    print(psutil.cpu_percent(interval=0.5, percpu=True))
```

# 2. 查询内存信息

```python
# 输出内存使用情况（总内存、可用内存、内存使用率、已使用内存）。
psutil.virtual_memory()
```

# 3. 查询磁盘信息

```python
# 磁盘分区信息
psutil.disk_partitions()

# 磁盘使用情况
psutil.disk_usage('/')

# 磁盘IO
psutil.disk_io_counters()
```

# 4. 查询网络信息

```python
# 查询网络读写字节／包的个数。
psutil.net_io_counters()
```

# 5. 查询进程信息

```python
psutil.pids() # 所有进程ID
```



```python
# 获取指定进程ID=113408
p = psutil.Process(113408)

# 进程名称
p.name()

# 进程的exe路径
p.exe()

# 进程的工作目录
p.cwd()

# 进程启动的命令行
p.cmdline()

# 当前进程id
p.pid
```

