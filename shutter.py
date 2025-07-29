#!/usr/bin/env python3
"""Simple shutter script triggered by a GPIO button."""

from __future__ import annotations

import datetime
import logging
import subprocess
from pathlib import Path

from gpiozero import Button  # works fine for any switch
from signal import pause

PHOTO_DIR = Path.home() / "Shutter" / "photos"
PHOTO_DIR.mkdir(parents=True, exist_ok=True)

# --- Adjust these two lines if you wired NC instead of NO -------------
button = Button(17, pull_up=True, bounce_time=0.05)   # COM+NO version
# button = Button(17, pull_up=True, bounce_time=0.05, active_state=False)  # COM+NC version
# ----------------------------------------------------------------------

def snap() -> None:
    """Capture a photo and store it in ``PHOTO_DIR``."""

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = PHOTO_DIR / f"{timestamp}.jpg"
    subprocess.run(
        [
            "rpicam-jpeg",
            "-n",
            "--autofocus-mode",
            "auto",
            "-t",
            "5000",
            "-o",
            str(outfile),
        ],
        check=True,
    )
    logging.info("Saved photo to %s", outfile)

def main() -> None:
    """Configure the GPIO button and wait for presses."""

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    button.when_pressed = snap
    logging.info("Limit-switch shutter armed.")
    pause()


if __name__ == "__main__":
    main()
