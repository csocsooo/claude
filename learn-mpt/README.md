# learn-mpt — MoneyPrinterTurbo minimál klón

Tanuló célú, futtatható újraépítése a [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)
pipeline-jának — a zaj nélkül. Téma → kész, feliratos, függőleges (Shorts/Reels/TikTok) videó.

```
téma → [LLM] script → [LLM] kulcsszavak → [TTS] hang
     → [Whisper] felirat → [Pexels] klipek → [ffmpeg] kész videó
```

## Mit lehet tanulni belőle?

| Fájl | Tanulság |
|------|----------|
| `mpt/pipeline.py` | A **`stop_at`-os futószalag** — ugyanaz a kód bármelyik lépés után leáll (debug + teszt). Ez a projekt szíve. |
| `mpt/llm.py` | **Provider-absztrakció**: bármilyen OpenAI-kompatibilis végpont (OpenAI, Groq, Ollama) + defenzív válasz-tisztítás (`<think>` blokkok). |
| `mpt/tts.py` | Ingyenes Edge-TTS, kulcs nélkül. |
| `mpt/subtitle.py` | Lokális Whisper hang→felirat, és a két felirat-megközelítés magyarázata. |
| `mpt/material.py` | Stock videó keresés + képarány-tudatos felbontásválasztás. |
| `mpt/render.py` | MoviePy összevágás, képarány-igazítás (crop, nem letterbox), **defenzív feliratégetés** (font hiányában is működik). |

Az eredetihez képest szándékosan KIMARADT: 20 LLM provider, 6 TTS backend, Redis,
GPU codec-kezelés, WebUI, auto-feltöltés. Ezek adják az eredeti komplexitásának
nagy részét, de a lényegből keveset.

## Telepítés

```bash
cd learn-mpt
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# ffmpeg szükséges a rendszeren (pl. apt install ffmpeg)
```

## Kulcsok (env változók)

| Változó | Kell? | Mire |
|---------|-------|------|
| `LLM_API_KEY` | igen* | script + kulcsszó (`*` Ollamánál bármi lehet) |
| `LLM_BASE_URL` | nem | alap: OpenAI; pl. `http://localhost:11434/v1` Ollamához |
| `LLM_MODEL` | nem | alap: `gpt-4o-mini` |
| `PEXELS_API_KEY` | igen | stock klipek (ingyenes: pexels.com/api) |

TTS és felirat **nem igényel kulcsot**.

## Használat

```bash
# Teljes videó
python main.py "A méhek szerepe az ökoszisztémában"

# Csak a scriptet nézzük meg (kulcsszó/hang/render nélkül)
python main.py "Why the sky is blue" --stop-at script

# Magyar hang, vízszintes képarány
python main.py "Kávé története" --voice hu-HU-NoemiNeural --aspect 16:9
```

A `--stop-at` választható értékei: `script`, `terms`, `audio`, `subtitle`, `materials`, `video`.

> Tanulási projekt, nem produkciós eszköz. A generált tartalom és a stock anyagok
> felhasználásánál tartsd be a Pexels és az adott platform feltételeit.
