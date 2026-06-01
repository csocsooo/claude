"""LLM réteg – script és kulcsszó generálás.

Az eredeti MoneyPrinterTurbo ~20 providert támogat (OpenAI, Gemini, Qwen,
DeepSeek, Ollama, g4f, ...). Mi EGY absztrakciót tartunk meg: bármilyen
OpenAI-kompatibilis végpontot használunk (`base_url` + `api_key`), így ugyanaz
a kód megy OpenAI-jal, Groqkal, helyi Ollamával stb.

Megtartott tanulság az eredetiből: a modell válaszát mindig defenzíven
tisztítjuk – kiszedjük a reasoning-modellek `<think>...</think>` blokkjait,
és kezeljük az üres/hibás választ.
"""

import re

from openai import OpenAI

from .config import config

# Reasoning modellek (DeepSeek-R1, QwQ, ...) belső gondolkodása – nem kell a scriptbe.
_THINK_BLOCK = re.compile(r"<think\b[^>]*>.*?</think>", re.IGNORECASE | re.DOTALL)

_SCRIPT_SYSTEM_PROMPT = """
# Szerep: Videó szkript generátor

## Cél
Írj egy felmondható narrációt a megadott témáról.

## Szabályok
1. Pontosan a kért számú bekezdés legyen.
2. Ne hivatkozz erre az utasításra, és ne említsd, hogy ez egy szkript.
3. Térj rögtön a lényegre – semmi "üdvözöllek a videóban" típusú bevezető.
4. Semmi markdown, cím vagy formázás – csak nyers, felolvasható szöveg.
5. Ne írj ki "narrátor:" / "voiceover:" jelölőket.
6. Válaszolj ugyanazon a nyelven, amin a téma van.
""".strip()


def _client() -> OpenAI:
    if not config.llm_api_key:
        raise RuntimeError(
            "Hiányzik az LLM_API_KEY. Állítsd be env változóként, vagy használj "
            "helyi Ollamát: LLM_BASE_URL=http://localhost:11434/v1 LLM_API_KEY=ollama"
        )
    return OpenAI(api_key=config.llm_api_key, base_url=config.llm_base_url)


def _chat(prompt: str, system: str = "") -> str:
    """Egy kör chat, defenzív válasz-tisztítással."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = _client().chat.completions.create(model=config.llm_model, messages=messages)

    if not resp.choices:
        raise ValueError("Az LLM üres választ adott (nincs choices).")
    content = resp.choices[0].message.content
    if not content:
        raise ValueError("Az LLM üres szöveget adott.")

    content = _THINK_BLOCK.sub("", content).strip()
    if not content:
        raise ValueError("Az LLM csak reasoning blokkot adott, érdemi szöveg nélkül.")
    return content


def generate_script(subject: str, paragraph_number: int) -> str:
    """A téma alapján megírja a videó narrációját."""
    prompt = (
        f"Téma: {subject}\n"
        f"Írj {paragraph_number} bekezdést, összesen kb. {paragraph_number * 2} mondatot."
    )
    return _chat(prompt, system=_SCRIPT_SYSTEM_PROMPT)


def generate_terms(subject: str, script: str, amount: int = 5) -> list[str]:
    """Stock-videó kereséshez angol kulcsszavakat ad (a Pexels angolul keres jól)."""
    prompt = (
        f"A téma: '{subject}'.\nA szkript:\n{script}\n\n"
        f"Adj pontosan {amount} db ANGOL keresőkulcsot stock videókhoz. "
        f"Egy-két szavasak legyenek, vesszővel elválasztva, semmi más szöveg."
    )
    raw = _chat(prompt)
    terms = [t.strip() for t in re.split(r"[,，\n]", raw) if t.strip()]
    return terms[:amount]
