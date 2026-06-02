"""Szöveg → beszéd (TTS) az ingyenes Microsoft Edge hangokkal.

Két dolgot ad vissza:
- a felmondott hangot (mp3),
- a SZÓ-SZINTŰ időbélyegeket (word boundaries).

Az időbélyegek a kulcs a pontos felirathoz: nem kell visszafejteni a hangot
Whisperrel (ami hibázhat), mert pontosan tudjuk, melyik szó mikor hangzik el.
Ez az eredeti MoneyPrinterTurbo "edge" felirat-útjának a lényege.

A hang tempója/magassága/hangereje is hangolható (config / CLI), hogy ne legyen
annyira monoton.
"""

import asyncio

import edge_tts

from .config import config

# Edge a szó-időbélyegeket 100 nanoszekundumos "tick"-ekben adja → másodperc.
_TICKS_PER_SECOND = 10_000_000


def synthesize(text: str, out_path: str) -> list[dict]:
    """Felmondja a szöveget mp3-ba, és visszaadja a szó-időbélyegeket.

    Visszatérés: lista {"text": szó, "start": mp, "end": mp} elemekkel.
    """
    cues: list[dict] = []
    audio = bytearray()

    async def _run():
        communicate = edge_tts.Communicate(
            text=text,
            voice=config.voice_name,
            rate=config.voice_rate,
            pitch=config.voice_pitch,
            volume=config.voice_volume,
            boundary="WordBoundary",  # szó-szintű időbélyegek a pontos felirathoz
        )
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / _TICKS_PER_SECOND
                dur = chunk["duration"] / _TICKS_PER_SECOND
                cues.append({"text": chunk["text"], "start": start, "end": start + dur})

    asyncio.run(_run())

    with open(out_path, "wb") as f:
        f.write(audio)
    return cues
