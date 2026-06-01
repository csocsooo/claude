"""A futószalag – ez a projekt szíve.

Az eredeti MoneyPrinterTurbo `task.py`-jának egyszerűsített mása. A kulcsötlet a
`stop_at` paraméter: ugyanaz a kód le tud állni bármelyik lépés UTÁN, így
külön-külön tesztelhető a script / hang / felirat / klipek / kész videó.

    téma → script → kulcsszavak → hang → felirat → klipek → kész videó
"""

import os
from dataclasses import dataclass

from . import llm, material, render, subtitle, tts
from .config import config

# A lépések sorrendje – a `stop_at` ezek egyikére állítható.
STEPS = ["script", "terms", "audio", "subtitle", "materials", "video"]


@dataclass
class Result:
    script: str | None = None
    terms: list[str] | None = None
    audio_file: str | None = None
    audio_duration: float | None = None
    subtitle_file: str | None = None
    clips: list[str] | None = None
    video_file: str | None = None


def _audio_duration(path: str) -> float:
    """A hangfájl hossza másodpercben (a render is ezt használja indirekt módon)."""
    from moviepy import AudioFileClip

    with AudioFileClip(path) as a:
        return a.duration


def run(subject: str, out_dir: str, stop_at: str = "video") -> Result:
    """Végigfuttatja a futószalagot a `subject` témára, `stop_at`-ig."""
    if stop_at not in STEPS:
        raise ValueError(f"stop_at értéke {STEPS} egyike legyen, kaptam: {stop_at!r}")

    os.makedirs(out_dir, exist_ok=True)
    res = Result()

    # 1. Script
    print("## 1/6  script generálása")
    res.script = llm.generate_script(subject, config.paragraph_number)
    if stop_at == "script":
        return res

    # 2. Kulcsszavak (stock kereséshez)
    print("## 2/6  kulcsszavak generálása")
    res.terms = llm.generate_terms(subject, res.script)
    if stop_at == "terms":
        return res

    # 3. Hang (TTS)
    print("## 3/6  hang (TTS) generálása")
    res.audio_file = tts.synthesize(res.script, os.path.join(out_dir, "audio.mp3"))
    res.audio_duration = _audio_duration(res.audio_file)
    if stop_at == "audio":
        return res

    # 4. Felirat (Whisper)
    print("## 4/6  felirat generálása")
    res.subtitle_file = subtitle.create(
        res.audio_file, os.path.join(out_dir, "subtitle.srt")
    )
    if stop_at == "subtitle":
        return res

    # 5. Stock klipek letöltése
    print("## 5/6  stock klipek letöltése")
    res.clips = material.download_videos(
        res.terms, os.path.join(out_dir, "clips"), res.audio_duration
    )
    if stop_at == "materials":
        return res

    # 6. Végső videó
    print("## 6/6  videó renderelése")
    res.video_file = render.render(
        res.clips,
        res.audio_file,
        res.subtitle_file,
        os.path.join(out_dir, "final.mp4"),
    )
    print(f"✅ Kész: {res.video_file}")
    return res
