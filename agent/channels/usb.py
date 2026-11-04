"""Detect removable-drive mount changes on Windows.

This first version detects USB connection/removal. File-level extraction
monitoring and prevention are a follow-up implementation.
"""

import time

import psutil


def monitor(on_change, interval=2.0):
    previous = set()
    while True:
        current = {
            (partition.device, partition.mountpoint)
            for partition in psutil.disk_partitions()
            if "removable" in partition.opts.lower()
        }
        for device, mountpoint in current - previous:
            on_change("connected", device, mountpoint)
        for device, mountpoint in previous - current:
            on_change("disconnected", device, mountpoint)
        previous = current
        time.sleep(interval)
