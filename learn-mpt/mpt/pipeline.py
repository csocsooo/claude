"""A futószalag – ez a projekt szíve.

Az eredeti MoneyPrinterTurbo `task.py`-jának egyszerűsített mása. A kulcsötlet a
`stop_at` paraméter: ugyanaz a kód le tud állni bármelyik lépés UTÁN, így
külön-külön tesztelhető a script / hang / felirat / klipek / kész videó.

    téma → script → kulcsszavak → hang → felirat → klipek → kész videó
"""

import os
from dataclasses import dataclass

from . import comfyui, llm, material, render, subtitle, tts
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


def run(
    subject: str,
    out_dir: str,
    stop_at: str = "video",
    script: str | None = None,
    terms: list[str] | None = None,
) -> Result:
    """Végigfuttatja a futószalagot a `subject` témára, `stop_at`-ig.

    `script`: ha megadod, ezt a kész szöveget használja az LLM helyett (pl. élő
        adatból összerakott narráció). Ilyenkor az 1. lépés kimarad.
    `terms`: ha megadod, ezeket a kulcsszavakat használja a stock kereséshez az
        LLM helyett. Ilyenkor a 2. lépés kimarad (LLM kulcs sem kell hozzá).
    """
    if stop_at not in STEPS:
        raise ValueError(f"stop_at értéke {STEPS} egyike legyen, kaptam: {stop_at!r}")

    os.makedirs(out_dir, exist_ok=True)
    res = Result()

    # 1. Script (kész szöveg vagy LLM)
    if script:
        print("## 1/6  kész szkript használata (LLM kihagyva)")
        res.script = script.strip()
    else:
        print("## 1/6  script generálása")
        res.script = llm.generate_script(subject, config.paragraph_number)
    if stop_at == "script":
        return res

    # 2. Kulcsszavak (csak ha kell vizuál-kereséshez)
    if terms:
        print("## 2/6  megadott kulcsszavak használata (LLM kihagyva)")
        res.terms = terms
    elif config.video_source == "none":
        print("## 2/6  gradiens háttér – kulcsszavak nem kellenek")
        res.terms = []
    else:
        print("## 2/6  kulcsszavak generálása")
        res.terms = llm.generate_terms(subject, res.script)
    if stop_at == "terms":
        return res

    # 3. Hang (TTS) – a szó-időbélyegeket is visszakapjuk a pontos felirathoz
    print("## 3/6  hang (TTS) generálása")
    res.audio_file = os.path.join(out_dir, "audio.mp3")
    word_cues = tts.synthesize(res.script, res.audio_file)
    res.audio_duration = _audio_duration(res.audio_file)
    if stop_at == "audio":
        return res

    # 4. Felirat – a TTS szó-időbélyegeiből (pontos); Whisper csak fallback
    res.subtitle_file = os.path.join(out_dir, "subtitle.srt")
    if word_cues:
        print("## 4/6  felirat a TTS szó-időbélyegeiből (pontos)")
        subtitle.from_word_cues(word_cues, res.subtitle_file)
    else:
        print("## 4/6  felirat Whisperrel (fallback)")
        subtitle.create(res.audio_file, res.subtitle_file)
    if stop_at == "subtitle":
        return res

    # 5. Vizuál beszerzése a választott forrásból
    clips_dir = os.path.join(out_dir, "clips")
    if config.video_source == "comfyui":
        print("## 5/6  vizuál generálása helyi ComfyUI-jal")
        if comfyui.is_available():
            res.clips = comfyui.generate(res.terms, clips_dir)
        else:
            print(
                f"⚠️  A ComfyUI nem elérhető ({config.comfyui_url}). "
                "Indítsd el a saját gépeden, vagy válassz --source pexels/none-t. "
                "Most gradiens háttérre váltok."
            )
            res.clips = []
    elif config.video_source == "pexels":
        print("## 5/6  stock klipek letöltése (Pexels)")
        res.clips = material.download_videos(res.terms, clips_dir, res.audio_duration)
    else:  # "none"
        print("## 5/6  vizuál kihagyva – gradiens háttér lesz")
        res.clips = []
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
