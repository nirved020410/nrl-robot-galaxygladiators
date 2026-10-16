"""Observe both boards' serial logs without transmitting program commands."""
from datetime import datetime
from pathlib import Path
import time
import serial

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
output = Path("diagnostics") / f"both-start-{stamp}.txt"
ports = {}
started = time.monotonic()
try:
    with output.open("w", encoding="utf-8") as log:
        for name in ("COM13", "COM14"):
            connection = serial.Serial(port=None, baudrate=115200, timeout=0)
            connection.dtr = True  # Mark USB CDC terminal open for guarded logs.
            connection.rts = False
            connection.port = name
            connection.open()
            ports[name] = connection
        print("Recording controller COM13 and robot COM14 for 45 seconds.", flush=True)
        while time.monotonic() - started < 45:
            for name, connection in ports.items():
                block = connection.read(connection.in_waiting or 1)
                if block:
                    text = f"[{time.monotonic()-started:06.2f}s {name}] " + block.decode("utf-8", errors="replace")
                    log.write(text)
                    log.flush()
                    print(text, end="", flush=True)
            time.sleep(0.03)
finally:
    for connection in ports.values():
        connection.close()
print(f"\nSaved {output}")
