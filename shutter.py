#!/usr/bin/env python3
from gpiozero import Button           # works fine for any switch
from signal import pause
import datetime, subprocess
from pathlib import Path

PHOTO_DIR = Path("/home/alireza/Shutter/photos")
PHOTO_DIR.mkdir(exist_ok=True)

# --- Adjust these two lines if you wired NC instead of NO -------------
button = Button(17, pull_up=True, bounce_time=0.05)   # COM+NO version
# button = Button(17, pull_up=True, bounce_time=0.05, active_state=False)  # COM+NC version
# ----------------------------------------------------------------------

def snap():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = PHOTO_DIR / f"{ts}.jpg"
    subprocess.run(
        ["rpicam-jpeg", "-n", "--autofocus-mode", "auto", "-t", "5000", "-o", str(outfile)],
        check=True
    )
    print(f"[OK] {outfile}")

button.when_pressed = snap
print("Limit-switch shutter armed.")
pause()
