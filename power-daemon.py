#!/usr/bin/env python3
import time
import pathlib


if(pathlib.Path("/sys/bus/platform/devices/INTC1042:00").exists()):
    INTC_DEV = pathlib.Path("/sys/bus/platform/devices/INTC1042:00")
else:
    INTC_DEV = pathlib.Path("/sys/bus/platform/devices/INTC10A0:00")
RAPL_MMIO = pathlib.Path("/sys/class/powercap/intel-rapl-mmio/intel-rapl-mmio:0")
IMOK_FILE = INTC_DEV / "imok"

PL1_LIMIT = 130000000  # 130W
PL2_LIMIT = 157000000  # 157W


if not IMOK_FILE.exists():
    raise RuntimeError(
        "ACPI handshake file not found. Are you running on a supported Intel platform?"
    )

if not RAPL_MMIO.exists():
    raise RuntimeError(
        "RAPL MMIO power dir not found. Are you running on a supported Intel platform?"
    )

(RAPL_MMIO / "constraint_0_power_limit_uw").write_text(str(PL1_LIMIT))  # Set PL1 limit
(RAPL_MMIO / "constraint_1_power_limit_uw").write_text(str(PL2_LIMIT))  # Set PL2 limit


while True:
    # Keep ACPI handshake alive periodically every 15 seconds
    IMOK_FILE.write_text("1")
    time.sleep(15)
