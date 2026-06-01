"""Felirat generálás: hangból (.mp3) feliratfájl (.srt) faster-whisperrel.

A faster-whisper lokálisan fut (CPU-n is), kulcs nélkül. Az első futáskor
letölti a modellt (a "base" ~140 MB), utána offline megy.

Megjegyzés a két megközelítésről (ezt érdemes megérteni):
- Az Edge-TTS maga is ad szó-szintű időbélyegeket, így felirat készíthető a
  hanggal EGYÜTT, külön felismerés nélkül (ez az eredeti gyorsabb útja).
- Mi a tanulság kedvéért a robusztusabb, backend-független utat választjuk:
  a kész hangot visszafejtjük Whisperrel. Ez bármilyen hangra működik
  (akár saját felvételre is), cserébe lassabb.
"""

from faster_whisper import WhisperModel

from .config import config


def _format_ts(seconds: float) -> str:
    """Másodperc → SRT időbélyeg: HH:MM:SS,mmm"""
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def create(audio_file: str, subtitle_file: str) -> str:
    """A hangfájlt feliratozza, és .srt-be írja. Visszaadja a felirat útját."""
    model = WhisperModel(config.whisper_model, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_file, word_timestamps=True)

    lines: list[str] = []
    for i, seg in enumerate(segments, start=1):
        text = seg.text.strip()
        if not text:
            continue
        lines.append(str(i))
        lines.append(f"{_format_ts(seg.start)} --> {_format_ts(seg.end)}")
        lines.append(text)
        lines.append("")  # üres sor választ el két blokkot

    with open(subtitle_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return subtitle_file
