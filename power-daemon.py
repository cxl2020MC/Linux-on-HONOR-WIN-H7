#!/usr/bin/env python3
import pathlib
import time

I7_INTC_DEV = pathlib.Path("/sys/bus/platform/devices/INTC10A0:00")
U7_INTC_DEV = pathlib.Path("/sys/bus/platform/devices/INTC1042:00")

if I7_INTC_DEV.exists():
    print("找到 I7 INTC 设备")
    INTC_DEV = I7_INTC_DEV
elif U7_INTC_DEV.exists():
    print("找到 U7 INTC 设备")
    INTC_DEV = U7_INTC_DEV
else:
    raise RuntimeError("未找到 ACPI 握手文件。你是否在受支持的 Intel 平台上运行？")

RAPL_MMIO = pathlib.Path("/sys/class/powercap/intel-rapl-mmio/intel-rapl-mmio:0")
IMOK_FILE = INTC_DEV / "imok"

PL1_LIMIT = 130000000  # 130W
PL2_LIMIT = 157000000  # 157W


# if not IMOK_FILE.exists():
#     raise RuntimeError(
#         "ACPI handshake file not found. Are you running on a supported Intel platform?"
#     )

if not RAPL_MMIO.exists():
    raise RuntimeError(
        "未找到 RAPL MMIO power 文件夹。你是否在受支持的Intel平台上运行？"
    )

(RAPL_MMIO / "constraint_0_power_limit_uw").write_text(str(PL1_LIMIT))  # Set PL1 limit
(RAPL_MMIO / "constraint_1_power_limit_uw").write_text(str(PL2_LIMIT))  # Set PL2 limit


while True:
    # Keep ACPI handshake alive periodically every 15 seconds
    IMOK_FILE.write_text("1")
    time.sleep(15)
