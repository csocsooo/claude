"""ComfyUI backend – AI kép/videó generálás a TE helyi ComfyUI-oddal.

A ComfyUI egy node-alapú Stable Diffusion / video futtató, amit lokálisan, GPU-val
futtatsz (alapból http://127.0.0.1:8188). Ez a modul az ő HTTP API-ját vezérli:

  1. betölt egy workflow sablont (ComfyUI → Save (API Format) JSON),
  2. a jelenet promptját beírja a `__PROMPT__` helyőrző helyére (+ friss seed a
     `__SEED__` helyőrzőre, ha van),
  3. sorba teszi  (POST /prompt), és WebSocketen / pollozva megvárja a véget,
  4. letölti a kész képet/videót (GET /view).

Így a learn-mpt a SAJÁT gépeden, a TE modelljeiddel és workflow-iddal dolgozik.

Megjegyzés: a felhős sandboxban (ahol ez a repo épült) nincs GPU és nincs
ComfyUI, ezért ott ez a modul nem fut – a saját gépeden viszont igen, ott ahol
amúgy is generálsz képeket/videókat.
"""

import json
import os
import time
import urllib.parse
import uuid

import requests

from .config import config

# Mely fájlnév-mezőkben szokott megjelenni a kész média a /history kimenetben.
_OUTPUT_KEYS = ("images", "gifs", "videos")
_IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp")


def _load_workflow(prompt: str, seed: int) -> dict:
    """Beolvassa a workflow sablont és behelyettesíti a prompt + seed helyőrzőket."""
    if not config.comfyui_workflow or not os.path.isfile(config.comfyui_workflow):
        raise RuntimeError(
            "Nincs ComfyUI workflow megadva. Exportáld a workflow-t a ComfyUI-ban "
            "(Save (API Format)), és add meg: COMFYUI_WORKFLOW=/út/workflow.json. "
            "A pozitív prompt mezőbe írj __PROMPT__ helyőrzőt."
        )
    raw = open(config.comfyui_workflow, encoding="utf-8").read()
    # Szöveges szintű csere – backend-független (kép- és videó-workflow-ra is jó).
    raw = raw.replace("__PROMPT__", json.dumps(prompt)[1:-1])  # JSON-escape
    raw = raw.replace("__SEED__", str(seed))
    return json.loads(raw)


def _queue(workflow: dict, client_id: str) -> str:
    resp = requests.post(
        f"{config.comfyui_url}/prompt",
        json={"prompt": workflow, "client_id": client_id},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["prompt_id"]


def _wait(prompt_id: str, timeout: float = 600.0) -> dict:
    """Megvárja, amíg a prompt elkészül, és visszaadja a /history kimenetét."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = requests.get(f"{config.comfyui_url}/history/{prompt_id}", timeout=30)
        resp.raise_for_status()
        history = resp.json()
        if prompt_id in history:
            return history[prompt_id]["outputs"]
        time.sleep(1.5)
    raise TimeoutError(f"ComfyUI prompt időtúllépés: {prompt_id}")


def _download_outputs(outputs: dict, out_dir: str, index: int) -> list[str]:
    """A /history kimenetből letölti az összes generált fájlt."""
    saved: list[str] = []
    for node_output in outputs.values():
        for key in _OUTPUT_KEYS:
            for item in node_output.get(key, []):
                params = {
                    "filename": item["filename"],
                    "subfolder": item.get("subfolder", ""),
                    "type": item.get("type", "output"),
                }
                url = f"{config.comfyui_url}/view?" + urllib.parse.urlencode(params)
                data = requests.get(url, timeout=120).content
                ext = os.path.splitext(item["filename"])[1] or ".png"
                dest = os.path.join(out_dir, f"comfy_{index:02d}_{len(saved)}{ext}")
                with open(dest, "wb") as f:
                    f.write(data)
                saved.append(dest)
    return saved


def is_available() -> bool:
    """Igaz, ha a helyi ComfyUI elérhető."""
    try:
        requests.get(f"{config.comfyui_url}/system_stats", timeout=3).raise_for_status()
        return True
    except Exception:
        return False


def generate(prompts: list[str], out_dir: str) -> list[str]:
    """Jelenetenként egy-egy promptból képet/videót generál a helyi ComfyUI-jal.

    Visszaadja a letöltött média (kép vagy videó) fájlok útját, sorrendben.
    """
    os.makedirs(out_dir, exist_ok=True)
    client_id = uuid.uuid4().hex
    media: list[str] = []
    for i, prompt in enumerate(prompts):
        seed = uuid.uuid4().int % (2**31)
        print(f"   → ComfyUI generálás {i + 1}/{len(prompts)}: {prompt[:60]}")
        workflow = _load_workflow(prompt, seed)
        prompt_id = _queue(workflow, client_id)
        outputs = _wait(prompt_id)
        media.extend(_download_outputs(outputs, out_dir, i))
    return media


def is_image(path: str) -> bool:
    return path.lower().endswith(_IMAGE_EXT)
