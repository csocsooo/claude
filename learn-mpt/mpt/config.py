"""Konfiguráció – API kulcsok és alapbeállítások egy helyen.

Tanulság az eredetiből: a kulcsokat SOHA ne égesd a kódba. Itt env változókból
olvassuk, így a repóba semmi titok nem kerül. Csak az LLM-hez és a Pexelshez
kell kulcs; a TTS (edge-tts) és a felirat (faster-whisper) teljesen ingyenes.
"""

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    # --- LLM (OpenAI-kompatibilis bármelyik végpont: OpenAI, Groq, Ollama, ...) ---
    llm_api_key: str = field(default_factory=lambda: os.getenv("LLM_API_KEY", ""))
    llm_base_url: str = field(
        default_factory=lambda: os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    )
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o-mini"))

    # --- Stock videó forrás ---
    pexels_api_key: str = field(default_factory=lambda: os.getenv("PEXELS_API_KEY", ""))

    # --- TTS (ingyenes, kulcs nélkül) ---
    # Magyar hang: "hu-HU-NoemiNeural". Lista: `edge-tts --list-voices`.
    voice_name: str = field(default_factory=lambda: os.getenv("MPT_VOICE", "en-US-AvaNeural"))

    # --- Felirat (faster-whisper, lokálisan fut, kulcs nélkül) ---
    whisper_model: str = field(default_factory=lambda: os.getenv("WHISPER_MODEL", "base"))

    # --- Videó paraméterek ---
    aspect: str = "9:16"          # függőleges (Shorts/Reels/TikTok); lehet "16:9" is
    paragraph_number: int = 3      # hány bekezdés a scriptben
    max_clip_seconds: float = 5.0  # egy stock klipből max ennyit használunk

    def resolution(self) -> tuple[int, int]:
        """A kívánt kimeneti felbontás (szélesség, magasság)."""
        return (1080, 1920) if self.aspect == "9:16" else (1920, 1080)


config = Config()
