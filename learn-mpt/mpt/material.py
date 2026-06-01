"""Stock videó anyag letöltése a Pexels API-ról a kulcsszavak alapján.

Az eredeti Pexelst és Pixabay-t is támogat; mi a Pexelst tartjuk meg (ingyenes
kulcs, bőséges kvóta). A logika: a kulcsszavakra videókat keresünk, és annyit
töltünk le, amennyi kitölti a hang hosszát.
"""

import os

import requests

from .config import config

_SEARCH_URL = "https://api.pexels.com/videos/search"


def _orientation() -> str:
    return "portrait" if config.aspect == "9:16" else "landscape"


def _search_one(term: str) -> str | None:
    """Egy kulcsszóra megkeresi a legjobb illeszkedő videó letöltési linkjét."""
    if not config.pexels_api_key:
        raise RuntimeError("Hiányzik a PEXELS_API_KEY env változó.")

    headers = {"Authorization": config.pexels_api_key}
    params = {"query": term, "per_page": 5, "orientation": _orientation()}
    resp = requests.get(_SEARCH_URL, headers=headers, params=params, timeout=30)
    resp.raise_for_status()

    target_w, target_h = config.resolution()
    for video in resp.json().get("videos", []):
        # A több felbontás közül a célhoz legközelebbit (de nem kisebbet) választjuk.
        files = sorted(video.get("video_files", []), key=lambda f: f.get("width", 0))
        for vf in files:
            if vf.get("width", 0) >= target_w * 0.8 and vf.get("link"):
                return vf["link"]
        if files and files[-1].get("link"):
            return files[-1]["link"]
    return None


def _download(url: str, dest: str) -> str:
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    return dest


def download_videos(terms: list[str], out_dir: str, audio_duration: float) -> list[str]:
    """Annyi klipet tölt le a kulcsszavakra, hogy lefedjék a hang hosszát.

    A klipekből később max `config.max_clip_seconds` használunk fejenként, ezért
    durván ennyi klip kell: hang_hossz / max_clip_seconds (+1 ráhagyás).
    """
    os.makedirs(out_dir, exist_ok=True)
    needed = int(audio_duration / config.max_clip_seconds) + 1

    paths: list[str] = []
    seen: set[str] = set()
    # Sorban végigmegyünk a kulcsszavakon, amíg össze nem gyűlik elég egyedi klip
    # vagy el nem fogynak a kulcsszavak (így nincs végtelen ciklus).
    for term in terms:
        if len(paths) >= needed:
            break
        link = _search_one(term)
        if not link or link in seen:
            continue
        seen.add(link)
        dest = os.path.join(out_dir, f"clip_{len(paths):02d}.mp4")
        paths.append(_download(link, dest))
    return paths
