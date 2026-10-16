"""Capture controller status while diagnosing menu selection; send no commands."""
from datetime import datetime
from pathlib import Path
import time
import serial

connection = serial.Serial(port=None, baudrate=115200, timeout=0.1)
connection.dtr = False
connection.rts = False
connection.port = "COM13"
data = bytearray()
try:
    connection.open()
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        block = connection.read(connection.in_waiting or 1)
        if block:
            data.extend(block)
            print(block.decode("utf-8", errors="replace"), end="", flush=True)
finally:
    connection.close()
output = Path("diagnostics") / ("controller-menu-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt")
output.write_bytes(data)
print(f"\nSaved {len(data)} bytes to {output}")
