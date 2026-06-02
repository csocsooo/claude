"""CLI belépési pont.

Példák:
    python main.py "A méhek szerepe az ökoszisztémában"
    python main.py "Why the sky is blue" --stop-at script
    python main.py "Coffee history" --out ./kimenet --stop-at audio
"""

import argparse
import os

from mpt.config import config
from mpt.pipeline import STEPS, run


def main():
    parser = argparse.ArgumentParser(description="MoneyPrinterTurbo minimál klón")
    parser.add_argument("subject", help="A videó témája")
    parser.add_argument("--out", default="./output", help="Kimeneti mappa")
    parser.add_argument(
        "--stop-at",
        default="video",
        choices=STEPS,
        help="Melyik lépés után álljon le (debughoz hasznos)",
    )
    parser.add_argument("--voice", help=f"TTS hang (alap: {config.voice_name})")
    parser.add_argument("--aspect", choices=["9:16", "16:9"], help="Képarány")
    parser.add_argument(
        "--script",
        help="Kész narráció szövege vagy egy .txt fájl útja (LLM kihagyva)",
    )
    parser.add_argument(
        "--terms",
        help="Stock-kereső kulcsszavak vesszővel (LLM kihagyva), pl. 'bitcoin,trading'",
    )
    args = parser.parse_args()

    if args.voice:
        config.voice_name = args.voice
    if args.aspect:
        config.aspect = args.aspect

    # A --script lehet maga a szöveg, vagy egy .txt fájl útja.
    script = args.script
    if script and os.path.isfile(script):
        script = open(script, encoding="utf-8").read()

    terms = [t.strip() for t in args.terms.split(",") if t.strip()] if args.terms else None

    result = run(
        args.subject, out_dir=args.out, stop_at=args.stop_at, script=script, terms=terms
    )

    print("\n--- Eredmény ---")
    if result.script:
        print(f"Script:\n{result.script}\n")
    if result.terms:
        print(f"Kulcsszavak: {result.terms}")
    if result.audio_file:
        print(f"Hang: {result.audio_file} ({result.audio_duration:.1f}s)")
    if result.subtitle_file:
        print(f"Felirat: {result.subtitle_file}")
    if result.clips:
        print(f"Klipek: {len(result.clips)} db")
    if result.video_file:
        print(f"Videó: {result.video_file}")


if __name__ == "__main__":
    main()
