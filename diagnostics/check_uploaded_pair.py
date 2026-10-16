"""Read boot/link output only; never send movement or program-start commands."""
import time
from pathlib import Path
import serial

ports = {}
lines = {"COM13": bytearray(), "COM14": bytearray()}
try:
    for name in lines:
        connection = serial.Serial(port=None, baudrate=115200, timeout=0)
        connection.dtr = False
        connection.rts = False
        connection.port = name
        connection.open()
        ports[name] = connection
    deadline = time.monotonic() + 12
    while time.monotonic() < deadline:
        for name, connection in ports.items():
            lines[name].extend(connection.read(connection.in_waiting or 1))
        time.sleep(0.05)
finally:
    for connection in ports.values():
        connection.close()

output = []
for name, data in lines.items():
    text = data.decode("utf-8", errors="replace")
    output.append(f"=== {name} ===\n{text}")
    print(f"{name}: {len(data)} bytes")
    print(text[-5000:])
Path("saved-versions/005-course-order/post-upload-serial.txt").write_text(
    "\n".join(output), encoding="utf-8"
)
