"""Szöveg → beszéd (TTS) az ingyenes Microsoft Edge hangokkal.

Az edge-tts a böngésző "Felolvasás" funkciójának hangjait éri el, kulcs és
fizetés nélkül, jó minőségben, sok nyelven (magyarul is: hu-HU-NoemiNeural).

Az eredeti projekt itt 6 backendet kínál (Edge, Azure, SiliconFlow, Gemini,
MiMo, ...). Nekünk a legjobb ár/érték az Edge, ezért csak azt tartjuk meg.
"""

import asyncio

import edge_tts

from .config import config


def synthesize(text: str, out_path: str) -> str:
    """A szöveget mp3-ba mondja fel. Visszaadja a fájl elérési útját."""

    async def _run():
        communicate = edge_tts.Communicate(text=text, voice=config.voice_name)
        await communicate.save(out_path)

    asyncio.run(_run())
    return out_path
