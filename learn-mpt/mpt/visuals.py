"""Vizuális segédek: betűtípus-keresés, gradiens háttér, kép → mozgó klip.

Ezek a forrás-független építőkockák: akár ComfyUI-képekből, akár háttérként
használjuk őket. A ComfyUI állóképeit itt keltjük életre lassú zoommal
(Ken Burns-effekt), hogy ne hassanak statikusnak.
"""

import glob
import os

import numpy as np
from moviepy import CompositeVideoClip, ImageClip

from .config import config

# Néhány gyakori betűtípus-hely Linuxon – az elsőt használjuk, amit megtalálunk.
_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def find_font() -> str | None:
    for path in _FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    hits = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
    return hits[0] if hits else None


def gradient_background(duration: float):
    """Sötétkék függőleges gradiens háttér a cél-felbontásban."""
    w, h = config.resolution()
    top = np.array([15, 23, 42], dtype=float)      # mély éjkék
    bottom = np.array([30, 41, 82], dtype=float)   # kicsit világosabb kék
    ramp = np.linspace(0.0, 1.0, h)[:, None, None]
    column = (top[None, None, :] * (1 - ramp) + bottom[None, None, :] * ramp)
    frame = np.repeat(column, w, axis=1).astype("uint8")  # (h, w, 3)
    return ImageClip(frame).with_duration(duration)


def image_to_clip(path: str, duration: float):
    """ComfyUI állóképből lassan ráközelítő (Ken Burns) videóklip."""
    target_w, target_h = config.resolution()
    img = ImageClip(path).with_duration(duration)

    # Kitöltés a célarányra (cover), majd lassú, középre tartó zoom.
    scale = max(target_w / img.w, target_h / img.h)
    base = img.resized(scale)
    zoomed = base.resized(lambda t: 1.0 + 0.06 * t / duration).with_position("center")
    return CompositeVideoClip([zoomed], size=(target_w, target_h)).with_duration(duration)
