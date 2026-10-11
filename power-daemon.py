#!/usr/bin/env python3
import time
# import os
import pathlib

INTC_DEV = "/sys/bus/platform/devices/INTC10A0:00"
RAPL_MMIO = "/sys/class/powercap/intel-rapl-mmio/intel-rapl-mmio:0"


pathlib.Path(f"{RAPL_MMIO}/constraint_0_power_limit_uw").write_text("130000000")  # Set PL1 limit
pathlib.Path(f"{RAPL_MMIO}/constraint_1_power_limit_uw").write_text("157000000")  # Disable PL2 limit



while True:
    # Keep ACPI handshake alive periodically every 15 seconds
    pathlib.Path(f"{INTC_DEV}/imok").write_text("1")
    time.sleep(15)
