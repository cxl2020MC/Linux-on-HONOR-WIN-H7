# Linux-on-HONOR-WIN-H7

> 注意： 
> 
> 运行官方未正式支持和测试的系统存在安全风险
> 
> 包括但不限于：
> 
> 硬件烧毁，软件故障，保修失效

## 本仓库已经完成修复了的问题

1. 在 linux 下，CPU 功耗被异常锁定到PL1: 40W PL2: 50W


## 修复方案

### CPU 功耗

这个主要是由于 Windows 下 [英特尔®动态调谐技术（Intel® DTT）](https://www.intel.cn/content/www/cn/zh/support/articles/000102775/processors.html) 和 Linux 下 [thermald](https://github.com/intel/thermal_daemon) 实现有着细微差别导致的

> 注：为了设备安全，请使用 intel 的 thermald 对设备进行温度控制和保护， 并且应用正确的 dtt 策略
> 并且保证 termald 添加了 `--adaptive` 参数
> 
> [相关文档](https://man.archlinux.org/man/thermald.8#adaptive)

主要缺失的东西就只有一个，在 `/sys/bus/platform/devices/INTC10A0:00` 下有个 `imok` 接口，只需要往内部定时写入 `1` 告诉 EC DTT 驱动正在正常运行。

所以非常简单的就可以得出解决方案
为本仓库目录下的 [power-daemon.py](power-daemon.py) 添加为系统服务并且开机自启动， 并且按照上文配置好 termald 服务

代码里面启动的时候写 PL1, PL2 功耗墙是为了，保证性能不会被 mmio-rapl 限制

## 相关资料

[rs0x29a/Linux-on-HONOR-MagicBook-14-Pro-2026-AI_ZQC-P_M1010](https://github.com/rs0x29a/Linux-on-HONOR-MagicBook-14-Pro-2026-AI_ZQC-P_M1010/blob/main/patch/fan/README.md#why-windows-behaves-differently) 这个仓库很多的东西对这台机器都有用

