"""Videó összeállítás MoviePy-jal (ffmpeg háttérrel).

Lépések:
1. A letöltött klipeket a cél-képarányra igazítjuk (resize + középre vágás).
2. Mindegyikből legfeljebb `max_clip_seconds` darabot veszünk, és egymás után
   fűzzük őket, amíg el nem érik a hang hosszát.
3. Ráhúzzuk a TTS hangot (és a videót a hang hosszára vágjuk).
4. Ha van felirat és elérhető betűtípus, ráégetjük a .srt-t.

Tanulság az eredetiből: a feliratégetés a legtörékenyebb rész (betűtípus kell
hozzá), ezért defenzíven kezeljük – ha nincs használható font, a videó felirat
nélkül, de hibátlanul elkészül (a .srt fájl külön akkor is megvan).
"""

import itertools
import os

from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    TextClip,
    VideoFileClip,
    concatenate_videoclips,
)

from . import comfyui, visuals
from .config import config


def _fit_to_aspect(clip: VideoFileClip):
    """A klipet a cél-felbontásra igazítja: kitölti, majd középre vágja (no letterbox)."""
    target_w, target_h = config.resolution()
    scale = max(target_w / clip.w, target_h / clip.h)
    resized = clip.resized(scale)
    return resized.cropped(
        width=target_w,
        height=target_h,
        x_center=resized.w / 2,
        y_center=resized.h / 2,
    )


def _parse_srt(path: str) -> list[tuple[float, float, str]]:
    """Minimál SRT-olvasó: (start, end, szöveg) hármasok listája."""

    def to_sec(ts: str) -> float:
        ts = ts.replace(",", ".")
        h, m, s = ts.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    items: list[tuple[float, float, str]] = []
    blocks = open(path, encoding="utf-8").read().strip().split("\n\n")
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        start, end = lines[1].split(" --> ")
        text = " ".join(lines[2:]).strip()
        items.append((to_sec(start), to_sec(end), text))
    return items


def _media_to_clip(path: str, max_duration: float):
    """Egy médiafájlból (ComfyUI kép vagy videó) a célarányra igazított klip."""
    if comfyui.is_image(path):
        # Állókép → Ken Burns mozgás, hogy ne legyen statikus.
        return visuals.image_to_clip(path, duration=max_duration)
    raw = VideoFileClip(path)
    return _fit_to_aspect(raw).subclipped(0, min(max_duration, raw.duration))


def _burn_subtitles(video, subtitle_path: str):
    """Ráégeti a feliratot. Ha nincs használható betűtípus, az eredetit adja vissza."""
    font = visuals.find_font()
    if not font:
        print("⚠️  Nincs használható betűtípus – a videó felirat nélkül készül.")
        return video

    _, target_h = config.resolution()
    overlays = [video]
    for start, end, text in _parse_srt(subtitle_path):
        txt = (
            TextClip(
                text=text,
                font=font,
                font_size=int(target_h * 0.045),
                color="white",
                stroke_color="black",
                stroke_width=3,
                method="caption",
                size=(int(video.w * 0.9), None),
            )
            .with_start(start)
            .with_duration(max(0.1, end - start))
            .with_position(("center", int(target_h * 0.78)))
        )
        overlays.append(txt)
    return CompositeVideoClip(overlays)


def render(
    clip_paths: list[str],
    audio_file: str,
    subtitle_file: str,
    output_file: str,
) -> str:
    """Összeállítja a végső videót. Visszaadja a kimeneti fájl útját."""
    audio = AudioFileClip(audio_file)
    target_duration = audio.duration

    # 1-2. Klipek (ComfyUI kép/videó vagy stock) igazítása + darabolás, amíg ki
    #       nem töltik a hang hosszát.
    segments = []
    total = 0.0
    # Ha kevés a klip, ciklikusan ismételjük, amíg ki nem töltik a hang hosszát.
    for path in itertools.cycle(clip_paths) if clip_paths else []:
        if total >= target_duration or len(segments) > 300:
            break
        piece = _media_to_clip(path, config.max_clip_seconds)
        segments.append(piece)
        total += piece.duration

    if segments:
        video = concatenate_videoclips(segments, method="compose").subclipped(
            0, target_duration
        )
    else:
        # Fallback: nincs vizuál (nincs ComfyUI/kulcs) → gradiens háttér, hogy a
        # feliratos, hangos videó akkor is elkészüljön.
        print("⚠️  Nincs videóklip – gradiens háttéren renderelek.")
        video = visuals.gradient_background(target_duration)

    # 3. Hang rá, a videó pontosan a hang hosszára.
    video = video.with_audio(audio)

    # 4. Felirat ráégetése (ha van).
    if subtitle_file and os.path.exists(subtitle_file):
        video = _burn_subtitles(video, subtitle_file)

    video.write_videofile(
        output_file,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=os.cpu_count() or 2,
    )
    return output_file
