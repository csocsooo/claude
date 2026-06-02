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

from .config import config


def _format_ts(seconds: float) -> str:
    """Másodperc → SRT időbélyeg: HH:MM:SS,mmm"""
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _write_srt(blocks: list[tuple[float, float, str]], subtitle_file: str) -> str:
    lines: list[str] = []
    for i, (start, end, text) in enumerate(blocks, start=1):
        lines += [str(i), f"{_format_ts(start)} --> {_format_ts(end)}", text, ""]
    with open(subtitle_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return subtitle_file


def from_word_cues(
    cues: list[dict],
    subtitle_file: str,
    max_chars: int = 42,
    max_duration: float = 3.5,
) -> str:
    """Pontos felirat a TTS szó-időbélyegeiből (nincs felismerési hiba).

    A szavakat sorokba csoportosítja: új sor, ha túl hosszú lenne (max_chars),
    túl sokáig tartana (max_duration), vagy mondatvégi írásjel után vagyunk.
    """
    blocks: list[tuple[float, float, str]] = []
    cur_words: list[str] = []
    cur_start = 0.0
    cur_end = 0.0

    def flush():
        nonlocal cur_words
        if cur_words:
            blocks.append((cur_start, cur_end, " ".join(cur_words).strip()))
            cur_words = []

    for cue in cues:
        word = cue["text"]
        if not cur_words:
            cur_start = cue["start"]
        candidate = (" ".join(cur_words + [word])).strip()
        too_long = len(candidate) > max_chars
        too_slow = (cue["end"] - cur_start) > max_duration
        if cur_words and (too_long or too_slow):
            flush()
            cur_start = cue["start"]
        cur_words.append(word)
        cur_end = cue["end"]
        # Mondatvégi írásjel → zárjuk a sort.
        if word.endswith((".", "!", "?", "…")):
            flush()
    flush()

    return _write_srt(blocks, subtitle_file)


def create(audio_file: str, subtitle_file: str) -> str:
    """Fallback: hangból felirat Whisperrel (ha nincs szó-időbélyeg).

    Pontatlanabb, mint a `from_word_cues`, mert a hangot újra felismeri – ezért
    csak akkor használjuk, ha a TTS nem adott időbélyegeket (pl. saját hangfájl).
    """
    from faster_whisper import WhisperModel  # lusta import: csak fallbackhez kell

    model = WhisperModel(config.whisper_model, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_file, word_timestamps=True)
    blocks = [(s.start, s.end, s.text.strip()) for s in segments if s.text.strip()]
    return _write_srt(blocks, subtitle_file)
